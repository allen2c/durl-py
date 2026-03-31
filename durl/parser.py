import base64
import binascii
import dataclasses
import re
import urllib.parse
from collections.abc import Iterable, Mapping

_TOKEN_RE = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+$")
_MIME_TYPE_RE = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+$")


@dataclasses.dataclass(frozen=True, slots=True)
class DURLComponents:
    mime_type: str | None
    parameters: tuple[tuple[str, str], ...]
    is_base64: bool
    raw_data: str


def parse_durl(value: str) -> DURLComponents:
    if not value.startswith("data:"):
        raise ValueError("Not a valid data URL")

    try:
        header, raw_data = value[5:].split(",", 1)
    except ValueError as exc:
        raise ValueError("Not a valid data URL") from exc

    mime_type, parameters, is_base64 = _parse_header(header)
    return DURLComponents(
        mime_type=mime_type,
        parameters=parameters,
        is_base64=is_base64,
        raw_data=raw_data,
    )


def serialize_durl(components: DURLComponents) -> str:
    header_parts: list[str] = []
    if components.mime_type:
        header_parts.append(components.mime_type)

    header_parts.extend(f"{key}={value}" for key, value in components.parameters)
    if components.is_base64:
        header_parts.append("base64")

    header = ";".join(header_parts)
    if not components.mime_type and header:
        header = f";{header}"
    return f"data:{header},{components.raw_data}"


def build_durl(
    *,
    mime_type: str | None,
    data: bytes,
    parameters: Mapping[str, str] | None = None,
    is_base64: bool = True,
) -> DURLComponents:
    normalized_mime_type, normalized_parameters = normalize_durl_metadata(
        mime_type=mime_type,
        parameters=parameters,
    )
    if is_base64:
        raw_data = base64.b64encode(data).decode("ascii")
    else:
        raw_data = urllib.parse.quote_from_bytes(data, safe="")

    return DURLComponents(
        mime_type=normalized_mime_type,
        parameters=normalized_parameters,
        is_base64=is_base64,
        raw_data=raw_data,
    )


def decode_durl_data(components: DURLComponents) -> str | bytes:
    decoded_bytes: bytes
    if components.is_base64:
        _ensure_ascii(components.raw_data, "Base64 payload")
        try:
            decoded_bytes = base64.b64decode(components.raw_data, validate=True)
        except binascii.Error as exc:
            raise ValueError("Invalid base64 payload") from exc
    else:
        _validate_percent_encoding(components.raw_data, label="payload")
        decoded_bytes = urllib.parse.unquote_to_bytes(components.raw_data)

    charset = _get_charset(components.parameters)
    if charset is not None:
        try:
            return decoded_bytes.decode(charset)
        except LookupError as exc:
            raise ValueError(f"Unknown charset: {charset}") from exc
        except UnicodeDecodeError as exc:
            raise ValueError(
                f"Unable to decode payload with charset {charset}"
            ) from exc

    if _is_text_mime_type(components.mime_type):
        try:
            return decoded_bytes.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ValueError(
                "Text payload is not valid ASCII; specify a charset"
            ) from exc

    return decoded_bytes


def normalize_durl_metadata(
    *,
    mime_type: str | None,
    parameters: Mapping[str, str] | Iterable[tuple[str, str]] | None,
) -> tuple[str | None, tuple[tuple[str, str], ...]]:
    return (
        _normalize_mime_type(mime_type),
        _normalize_parameters(parameters),
    )


def _parse_header(header: str) -> tuple[str | None, tuple[tuple[str, str], ...], bool]:
    if not header:
        return None, (), False

    parts = header.split(";")
    mime_type = _normalize_mime_type(parts[0] or None)
    parameter_items: list[tuple[str, str]] = []
    seen_parameter_names: set[str] = set()
    is_base64 = False

    for part in parts[1:]:
        if not part:
            raise ValueError("Invalid data URL header")
        if part.lower() == "base64":
            if is_base64:
                raise ValueError("Duplicate base64 flag")
            is_base64 = True
            continue

        if is_base64:
            raise ValueError("Parameters must appear before the base64 flag")
        if "=" not in part:
            raise ValueError(f"Invalid parameter format: {part}")
        key, value = part.split("=", 1)
        normalized_key, normalized_value = _normalize_parameter(key, value)
        lowercase_key = normalized_key.lower()
        if lowercase_key in seen_parameter_names:
            raise ValueError(f"Duplicate parameter: {normalized_key}")
        seen_parameter_names.add(lowercase_key)
        parameter_items.append((normalized_key, normalized_value))

    return mime_type, tuple(parameter_items), is_base64


def _normalize_parameters(
    parameters: Mapping[str, str] | Iterable[tuple[str, str]] | None,
) -> tuple[tuple[str, str], ...]:
    if parameters is None:
        return ()

    items = parameters.items() if isinstance(parameters, Mapping) else parameters
    normalized_items: list[tuple[str, str]] = []
    seen_parameter_names: set[str] = set()

    for key, value in items:
        normalized_key, normalized_value = _normalize_parameter(key, value)
        lowercase_key = normalized_key.lower()
        if lowercase_key in seen_parameter_names:
            raise ValueError(f"Duplicate parameter: {normalized_key}")
        seen_parameter_names.add(lowercase_key)
        normalized_items.append((normalized_key, normalized_value))

    return tuple(normalized_items)


def _normalize_parameter(key: str, value: str) -> tuple[str, str]:
    key = key.strip()
    value = value.strip()
    if not key or not value:
        raise ValueError("Parameters must contain non-empty keys and values")
    if not _TOKEN_RE.fullmatch(key):
        raise ValueError(f"Invalid parameter name: {key}")

    _ensure_ascii(value, f"Parameter value for {key}")
    _validate_percent_encoding(value, label=f"parameter value for {key}")
    return key, value


def _normalize_mime_type(mime_type: str | None) -> str | None:
    if mime_type is None:
        return None

    normalized = mime_type.strip()
    if not normalized:
        return None
    if not _MIME_TYPE_RE.fullmatch(normalized):
        raise ValueError(f"Invalid media type: {normalized}")
    return normalized


def _is_text_mime_type(mime_type: str | None) -> bool:
    return mime_type is None or mime_type.startswith("text/")


def _get_charset(parameters: tuple[tuple[str, str], ...]) -> str | None:
    for key, value in parameters:
        if key.lower() == "charset":
            return value
    return None


def _validate_percent_encoding(value: str, *, label: str) -> None:
    _ensure_ascii(value, label.capitalize())

    index = 0
    while index < len(value):
        if value[index] != "%":
            index += 1
            continue
        if index + 2 >= len(value) or not _is_hex_pair(value[index + 1 : index + 3]):
            raise ValueError(f"Invalid percent-encoding in {label}")
        index += 3


def _ensure_ascii(value: str, label: str) -> None:
    try:
        value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{label} must contain only ASCII characters") from exc


def _is_hex_pair(value: str) -> bool:
    return len(value) == 2 and all(
        character in "0123456789ABCDEFabcdef" for character in value
    )
