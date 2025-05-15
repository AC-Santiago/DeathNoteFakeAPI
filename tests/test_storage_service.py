import pytest
from unittest.mock import patch
from fastapi import UploadFile
from app.services.storage import upload_photo
import io


@pytest.fixture
def mock_image_file():
    return UploadFile(
        filename="test.jpg",
        file=io.BytesIO(b"test image content"),
        content_type="image/jpeg",
    )


@pytest.mark.asyncio
async def test_upload_photo_success(mock_image_file):
    expected_url = "https://example.com/test.jpg"

    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {"url": expected_url}

        result = await upload_photo(mock_image_file)

        assert result == expected_url
        mock_upload.assert_called_once()


@pytest.mark.asyncio
async def test_upload_photo_failure(mock_image_file):
    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.side_effect = Exception("Upload failed")

        result = await upload_photo(mock_image_file)

        assert result is None
