import textwrap

from durl import DURL
from durl.utils.text import contents_from_text

RAW_CONTENT = textwrap.dedent("""
    Can you tell me what is in the image?data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==

    And how is the sound like?
    data:audio/mpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==

    And what is the text say?
    data:text/plain;base64,SGVsbG8sIHdvcmxkIQ==

    """).strip()  # noqa: E501


def test_durl_from_content() -> None:
    contents = contents_from_text(RAW_CONTENT)

    assert len(contents) == 6
    assert contents[0] == "Can you tell me what is in the image?"
    assert isinstance(contents[1], DURL)
    assert contents[1].mime_type == "image/png"
    assert contents[2] == "\n\nAnd how is the sound like?\n"
    assert isinstance(contents[3], DURL)
    assert contents[3].mime_type == "audio/mpeg"
    assert contents[4] == "\n\nAnd what is the text say?\n"
    assert isinstance(contents[5], DURL)
    assert contents[5].mime_type == "text/plain"
    assert contents[5].parsed_data == "Hello, world!"


def test_invalid_data_url_fragment_stays_text() -> None:
    content = "prefix data:text plain;base64,SGVsbG8= suffix"

    contents = contents_from_text(content)

    assert contents == [content]


def test_text_without_trailing_segment_does_not_add_empty_string() -> None:
    contents = contents_from_text("prefix data:text/plain;base64,SGVsbG8=")

    assert len(contents) == 2
    assert contents[0] == "prefix "
    assert isinstance(contents[1], DURL)


def test_text_without_any_data_url_returns_original_text_only() -> None:
    content = "plain text only"

    assert contents_from_text(content) == [content]
