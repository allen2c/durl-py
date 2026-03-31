import pytest

from durl import DURL


def test_parse_base64_data_url() -> None:
    durl = DURL("data:text/plain;base64,SGVsbG8=")

    assert durl.mime_type == "text/plain"
    assert durl.is_base64 is True
    assert durl.raw_data == "SGVsbG8="
    assert durl.parsed_data == "Hello"
    assert str(durl) == "data:text/plain;base64,SGVsbG8="


def test_parse_non_base64_with_charset() -> None:
    durl = DURL("data:text/plain;charset=UTF-8,%E4%BD%A0%E5%A5%BD")

    assert durl.parameters["charset"] == "UTF-8"
    assert durl.is_base64 is False
    assert durl.parsed_data == "你好"


def test_build_creates_base64_variant() -> None:
    durl = DURL.build(mime_type="text/plain", data=b"Hello")

    assert durl.mime_type == "text/plain"
    assert durl.is_base64 is True
    assert durl.raw_data == "SGVsbG8="
    assert str(durl) == "data:text/plain;base64,SGVsbG8="


def test_with_methods_return_new_instances() -> None:
    original = DURL("data:text/plain;base64,SGVsbG8=")
    updated = original.with_mime_type("text/markdown").with_parameters(
        {"charset": "UTF-8"}
    )

    assert original.mime_type == "text/plain"
    assert updated.mime_type == "text/markdown"
    assert dict(updated.parameters) == {"charset": "UTF-8"}
    assert original is not updated


def test_with_data_preserves_base64_mode() -> None:
    original = DURL("data:text/plain;base64,SGVsbG8=")
    updated = original.with_data(b"Hi")

    assert updated.is_base64 is True
    assert updated.raw_data == "SGk="
    assert updated.parsed_data == "Hi"


def test_invalid_base64_payload_raises() -> None:
    durl = DURL("data:text/plain;base64,***")

    with pytest.raises(ValueError, match="Invalid base64 payload"):
        _ = durl.parsed_data


def test_serialize_without_mime_type_keeps_leading_semicolon() -> None:
    durl = DURL.build(mime_type=None, data=b"Hello")

    assert str(durl) == "data:;base64,SGVsbG8="
