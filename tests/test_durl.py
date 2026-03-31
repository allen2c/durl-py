"""v0.3.0 contract tests. Canonical command: `python -m pytest -q`."""

import pytest

from durl import DURL


def test_constructs_from_base64_data_url() -> None:
    durl = DURL("data:text/plain;base64,SGVsbG8gV29ybGQ=")

    assert durl.mime_type == "text/plain"
    assert dict(durl.parameters) == {}
    assert durl.is_base64 is True
    assert durl.raw_data == "SGVsbG8gV29ybGQ="
    assert durl.parsed_data == "Hello World"
    assert durl.value == "data:text/plain;base64,SGVsbG8gV29ybGQ="


def test_constructs_from_non_base64_binary_data_url() -> None:
    durl = DURL("data:application/octet-stream,%00%FF%10")

    assert durl.mime_type == "application/octet-stream"
    assert durl.is_base64 is False
    assert durl.parsed_data == b"\x00\xff\x10"
    assert str(durl) == "data:application/octet-stream,%00%FF%10"


def test_constructs_from_non_base64_data_url_without_mime_type() -> None:
    durl = DURL("data:;charset=UTF-8,%E4%BD%A0%E5%A5%BD")

    assert durl.mime_type is None
    assert dict(durl.parameters) == {"charset": "UTF-8"}
    assert durl.is_base64 is False
    assert durl.parsed_data == "你好"
    assert str(durl) == "data:;charset=UTF-8,%E4%BD%A0%E5%A5%BD"


def test_build_defaults_to_base64_and_round_trips() -> None:
    durl = DURL.build(mime_type="text/plain", data=b"Hello World")

    assert durl.is_base64 is True
    assert durl.parsed_data == "Hello World"
    assert DURL(str(durl)).parsed_data == "Hello World"


def test_build_supports_non_base64_with_parameters() -> None:
    durl = DURL.build(
        mime_type="text/plain",
        data="你好".encode("utf-8"),
        parameters={"charset": "UTF-8", "format": "plain"},
        is_base64=False,
    )

    assert durl.is_base64 is False
    assert dict(durl.parameters) == {"charset": "UTF-8", "format": "plain"}
    assert durl.raw_data == "%E4%BD%A0%E5%A5%BD"
    assert durl.parsed_data == "你好"
    assert str(durl) == "data:text/plain;charset=UTF-8;format=plain,%E4%BD%A0%E5%A5%BD"


def test_build_without_mime_type_keeps_leading_semicolon() -> None:
    durl = DURL.build(mime_type=None, data=b"Hello")

    assert str(durl) == "data:;base64,SGVsbG8="


def test_with_methods_return_new_instances_and_preserve_original() -> None:
    original = DURL("data:text/plain;base64,SGVsbG8=")
    updated = (
        original.with_mime_type("text/markdown")
        .with_parameters({"charset": "UTF-8"})
        .with_raw_data("SGk=")
    )

    assert original.mime_type == "text/plain"
    assert dict(original.parameters) == {}
    assert original.raw_data == "SGVsbG8="
    assert updated.mime_type == "text/markdown"
    assert dict(updated.parameters) == {"charset": "UTF-8"}
    assert updated.raw_data == "SGk="
    assert updated.parsed_data == "Hi"


def test_with_data_preserves_encoding_mode() -> None:
    original = DURL("data:text/plain;charset=UTF-8,%E4%BD%A0%E5%A5%BD")
    updated = original.with_data("再見".encode("utf-8"))

    assert updated.is_base64 is False
    assert updated.raw_data == "%E5%86%8D%E8%A6%8B"
    assert updated.parsed_data == "再見"
    assert str(updated) == "data:text/plain;charset=UTF-8,%E5%86%8D%E8%A6%8B"


def test_parameters_mapping_is_read_only() -> None:
    durl = DURL("data:text/plain;charset=UTF-8,Hello")

    with pytest.raises(TypeError):
        durl.parameters["charset"] = "US-ASCII"  # type: ignore[index]


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ("https://example.com", "Not a valid data URL"),
        ("data:text/plain;base64", "Not a valid data URL"),
        ("data:text/plain;base64,***", "Invalid base64 payload"),
        ("data:text/plain,%E4%BD%A0%ZZ", "Invalid percent-encoding in payload"),
        (
            "data:text/plain;charset=NO_SUCH_CHARSET,Hello",
            "Unknown charset: NO_SUCH_CHARSET",
        ),
        (
            "data:text/plain,%E4%BD%A0%E5%A5%BD",
            "Text payload is not valid ASCII; specify a charset",
        ),
        (
            "data:text/plain;base64;charset=UTF-8,SGVsbG8=",
            "Parameters must appear before the base64 flag",
        ),
        (
            "data:text/plain;charset=UTF-8;charset=US-ASCII,Hello",
            "Duplicate parameter: charset",
        ),
        ("data:text plain;base64,SGVsbG8=", "Invalid media type"),
    ],
)
def test_invalid_inputs_raise_clear_errors(value: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        if not value.startswith("data:"):
            DURL(value)
        elif "payload" in message or "charset" in message:
            _ = DURL(value).parsed_data
        else:
            DURL(value)


def test_build_rejects_duplicate_parameter_names_case_insensitively() -> None:
    with pytest.raises(ValueError, match="Duplicate parameter: CHARSET"):
        DURL.build(
            mime_type="text/plain",
            data=b"Hello",
            parameters=[("charset", "UTF-8"), ("CHARSET", "US-ASCII")],
        )


def test_with_parameters_reuses_same_validation_as_parser() -> None:
    durl = DURL("data:text/plain;base64,SGVsbG8=")

    with pytest.raises(ValueError, match="Invalid media type"):
        durl.with_mime_type("text plain")

    with pytest.raises(ValueError, match="Duplicate parameter: CHARSET"):
        durl.with_parameters([("charset", "UTF-8"), ("CHARSET", "US-ASCII")])  # type: ignore[arg-type]


def test_repr_wraps_serialized_value() -> None:
    durl = DURL("data:text/plain;base64,SGVsbG8=")

    assert repr(durl) == "DURL('data:text/plain;base64,SGVsbG8=')"
