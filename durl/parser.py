import base64
import binascii
import dataclasses
import urllib.parse
from collections.abc import Mapping


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
        parameters=tuple(parameters.items()),
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
    normalized_parameters = _normalize_parameters(parameters)
    if is_base64:
        raw_data = base64.b64encode(data).decode("ascii")
    else:
        raw_data = urllib.parse.quote_from_bytes(data, safe="")

    return DURLComponents(
        mime_type=_normalize_mime_type(mime_type),
        parameters=tuple(normalized_parameters.items()),
        is_base64=is_base64,
        raw_data=raw_data,
    )


def decode_durl_data(components: DURLComponents) -> str | bytes:
    decoded_bytes: bytes
    if components.is_base64:
        try:
            decoded_bytes = base64.b64decode(components.raw_data, validate=True)
        except binascii.Error as exc:
            raise ValueError("Invalid base64 payload") from exc
    else:
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


def _parse_header(header: str) -> tuple[str | None, dict[str, str], bool]:
    if not header:
        return None, {}, False

    parts = header.split(";")
    mime_type = _normalize_mime_type(parts[0] or None)
    parameters: dict[str, str] = {}
    is_base64 = False

    for part in parts[1:]:
        if not part:
            raise ValueError("Invalid data URL header")
        if part.lower() == "base64":
            if is_base64:
                raise ValueError("Duplicate base64 flag")
            is_base64 = True
            continue

        if "=" not in part:
            raise ValueError(f"Invalid parameter format: {part}")
        key, value = part.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError(f"Invalid parameter format: {part}")
        parameters[key] = value

    return mime_type, parameters, is_base64


def _normalize_parameters(parameters: Mapping[str, str] | None) -> dict[str, str]:
    if parameters is None:
        return {}

    normalized: dict[str, str] = {}
    for key, value in parameters.items():
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError("Parameters must contain non-empty keys and values")
        normalized[key] = value
    return normalized


def _normalize_mime_type(mime_type: str | None) -> str | None:
    if mime_type is None:
        return None

    normalized = mime_type.strip()
    if not normalized:
        return None
    return normalized


def _is_text_mime_type(mime_type: str | None) -> bool:
    return mime_type is None or mime_type.startswith("text/")


def _get_charset(parameters: tuple[tuple[str, str], ...]) -> str | None:
    for key, value in parameters:
        if key.lower() == "charset":
            return value
    return None
