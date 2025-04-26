from typing import Optional
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status

from uuid import uuid4
import os
import tempfile


async def upload_photo(file: UploadFile) -> Optional[str]:
    """
    Sube una foto a Cloudinary y retorna la URL pública.

    Args:
        file: Archivo de imagen subido

    Returns:
        str: URL pública de la imagen

    Raises:
        HTTPException: Si hay un error al subir el archivo
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser una imagen",
        )

    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        upload_result = cloudinary.uploader.upload(
            temp_file_path,
            folder="death_note/fotos",
            public_id=str(uuid4()),
            overwrite=True,
        )

        os.unlink(temp_file_path)

        return upload_result["secure_url"]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir la imagen: {str(e)}",
        )
    finally:
        await file.close()
