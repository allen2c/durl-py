import base64
import tempfile

import pytest

from durl import DataURL, MIMEType


class TestDataURL:
    """Test suite for DataURL class."""

    def test_constructor_with_valid_data(self) -> None:
        """Test DataURL constructor with valid parameters."""
        data_url = DataURL(
            mime_type=MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N,
            data=base64.b64encode(b"Hello World").decode("utf-8"),
        )
        assert data_url.mime_type == MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N
        assert data_url.data == base64.b64encode(b"Hello World").decode("utf-8")
        assert data_url.encoded == "base64"

    def test_from_url_class_method(self) -> None:
        """Test DataURL.from_url class method with valid data URL."""
        url = "data:text/plain;base64,SGVsbG8gV29ybGQ="
        data_url = DataURL.from_url(url)
        assert data_url.mime_type == MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N
        assert data_url.data == "SGVsbG8gV29ybGQ="
        assert data_url.encoded == "base64"

    def test_from_data_class_method(self) -> None:
        """Test DataURL.from_data class method with raw data."""
        raw_data = "Hello World"
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, raw_data
        )
        assert data_url.mime_type == MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N
        assert data_url.data == base64.b64encode(b"Hello World").decode("utf-8")
        assert data_url.encoded == "base64"

    def test_is_data_url_class_method(self) -> None:
        """Test DataURL.is_data_url class method."""
        valid_url = "data:text/plain;base64,SGVsbG8gV29ybGQ="
        invalid_url = "https://example.com"
        assert DataURL.is_data_url(valid_url) is True
        assert DataURL.is_data_url(invalid_url) is False

    def test_url_property(self) -> None:
        """Test DataURL.url property returns correct URL string."""
        data_url = DataURL(
            mime_type=MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N,
            data=base64.b64encode(b"Hello World").decode("utf-8"),
        )
        expected_url = (
            f"data:text/plain;base64,{base64.b64encode(b'Hello World').decode('utf-8')}"
        )
        assert data_url.url == expected_url

    def test_data_decoded_property(self) -> None:
        """Test DataURL.data_decoded property returns decoded data."""
        raw_data = "Hello World"
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, raw_data
        )
        assert data_url.data_decoded == raw_data

    def test_data_decoded_bytes_property(self) -> None:
        """Test DataURL.data_decoded_bytes property returns decoded bytes."""
        raw_data = "Hello World"
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, raw_data
        )
        assert data_url.data_decoded_bytes == b"Hello World"

    def test_is_text_content_property(self) -> None:
        """Test DataURL.is_text_content property for text MIME type."""
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, "Hello"
        )
        assert data_url.is_text_content is True

    def test_is_image_content_property(self) -> None:
        """Test DataURL.is_image_content property for image MIME type."""
        data_url = DataURL.from_data(
            MIMEType.PORTABLE_NETWORK_GRAPHICS, b"fake_png_data"
        )
        assert data_url.is_image_content is True

    def test_is_audio_content_property(self) -> None:
        """Test DataURL.is_audio_content property for audio MIME type."""
        data_url = DataURL.from_data(MIMEType.MP3_AUDIO, b"fake_audio_data")
        assert data_url.is_audio_content is True

    def test_md5_property(self) -> None:
        """Test DataURL.md5 property returns MD5 hash of data."""
        raw_data = "Hello World"
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, raw_data
        )
        import hashlib

        expected_md5 = hashlib.md5(b"Hello World").hexdigest()
        assert data_url.md5 == expected_md5

    def test_str_method(self) -> None:
        """Test DataURL.__str__ method returns URL string."""
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, "Hello"
        )
        assert str(data_url) == data_url.url

    def test_save_method(self) -> None:
        """Test DataURL.save method saves data to file."""
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, "Hello World"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = data_url.save(tmpdir)
            assert filepath.exists()
            assert filepath.read_bytes() == b"Hello World"

    def test_url_truncated_property(self) -> None:
        """Test DataURL.url_truncated property returns truncated URL."""
        long_data = "x" * 200
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, long_data
        )
        truncated = data_url.url_truncated
        full_url = data_url.url
        # Test that truncation actually occurs for long URLs
        assert len(truncated) < len(full_url)
        # Test that the truncated version starts with the data URL prefix
        assert truncated.startswith("data:text/plain;base64,")

    def test_is_data_decoded_str_property(self) -> None:
        """Test DataURL.is_data_decoded_str property returns correct boolean."""
        text_data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, "Hello"
        )
        binary_data_url = DataURL.from_data(
            MIMEType.PORTABLE_NETWORK_GRAPHICS, b"\x89PNG"
        )
        assert text_data_url.is_data_decoded_str is True
        assert binary_data_url.is_data_decoded_str is False

    def test_from_url_with_invalid_url(self) -> None:
        """Test DataURL.from_url raises ValueError for invalid URL."""
        invalid_url = "https://example.com"
        with pytest.raises(ValueError, match="Not a valid data URL"):
            DataURL.from_url(invalid_url)

    def test_from_url_with_non_base64_encoding(self) -> None:
        """Test DataURL.from_url raises ValueError for non-base64 encoding."""
        invalid_url = "data:text/plain,Hello%20World"  # URL encoding instead of base64
        with pytest.raises(ValueError, match="Data URL must be base64 encoded"):
            DataURL.from_url(invalid_url)

    def test_validate_parameters_with_invalid_format(self) -> None:
        """Test parameter validation with invalid format."""
        with pytest.raises(ValueError, match="Invalid parameter format"):
            DataURL(
                mime_type=MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N,
                data="SGVsbG8=",
                parameters="invalid_param_without_equals",
            )

    def test_from_url_with_missing_mime_type(self) -> None:
        """Test DataURL.from_url raises ValueError for missing MIME type."""
        invalid_url = "data:;base64,SGVsbG8="
        with pytest.raises(ValueError, match="MIME type is required"):
            DataURL.from_url(invalid_url)

    def test_serialize_model_method(self) -> None:
        """Test DataURL model serialization returns URL string."""
        data_url = DataURL.from_data(
            MIMEType.TEXT_GENERALLY_ASCII_OR_ISO_8859_N, "Hello"
        )
        # Test that the Pydantic serialization returns the URL
        serialized = data_url.model_dump()
        assert serialized == data_url.url
