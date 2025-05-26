from fastapi import UploadFile, HTTPException
import uuid
import os
import aiofiles
from app.core.config import settings

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}

CHUNK_SIZE = 1024 * 1024  # 1 MB

async def upload_images(files: list[UploadFile]) -> list[str]: 
    saved_files = []

    for file in files:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Only JPEG and PNG images are allowed.")
        
        file_name = _generate_uuid_file_name(file.filename)
        file_path = os.path.join(settings.UPLOAD_DIR, file_name)

        async with aiofiles.open(file_path, "wb") as out_file:
            while chunk := await file.read(CHUNK_SIZE):
                await out_file.write(chunk)
        
        saved_files.append(file_name)    
   
    return saved_files

async def save_images_in_db(names: list[str]):
    pass

def _generate_uuid_file_name(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return f"{uuid.uuid4().hex}{ext}"
    
