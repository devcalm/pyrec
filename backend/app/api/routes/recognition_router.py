from fastapi import APIRouter, UploadFile, File, status
from app.deps import SessionDep, CurrentUser
from app.services.files import upload_images, save_images_in_db

router = APIRouter(prefix="/recognition", tags=["recognition"])

@router.post("/upload-images", status_code=status.HTTP_204_NO_CONTENT)
async def upload_images_router(
    user: CurrentUser, session: SessionDep, files: list[UploadFile] = File(...)
):
    images: list[str] = await upload_images(files)
    await save_images_in_db(user_id=user.id, names = images, session=session)
