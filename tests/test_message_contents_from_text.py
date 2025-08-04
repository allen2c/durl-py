import textwrap

from durl import DataURL, message_contents_from_text

RAW_CONTENT = textwrap.dedent(
    """
    Can you tell me what is in the image?data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==

    And how is the sound like?
    data:audio/mpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==

    And what is the text say?
    data:text/plain;base64,SGVsbG8sIHdvcmxkIQ==

    """  # noqa: E501
).strip()


def test_message_contents_from_text():
    contents = message_contents_from_text(RAW_CONTENT)
    assert len(contents) == 6
    assert any(c.is_text_content for c in contents if isinstance(c, DataURL))
    assert any(c.is_image_content for c in contents if isinstance(c, DataURL))
    assert any(c.is_audio_content for c in contents if isinstance(c, DataURL))

    for c in contents:
        if isinstance(c, DataURL):
            if c.is_text_content:
                assert c.data_decoded
                assert c.is_data_decoded_str
            elif c.is_image_content:
                assert c.data_decoded
            elif c.is_audio_content:
                assert c.data_decoded
            else:
                raise ValueError(f"Unknown data url: {c}")
