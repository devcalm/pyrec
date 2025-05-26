from fastapi import APIRouter, UploadFile, File, status
from app.deps import SessionDep
from app.services.files import upload_images

router = APIRouter(prefix="/recognition", tags=["recognition"])

@router.post("/upload-images", status_code=status.HTTP_204_NO_CONTENT)
async def upload_images_router(session: SessionDep, files: list[UploadFile] = File(...)):
    images: list[str] = await upload_images(files)
