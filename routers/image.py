from fastapi import status, Depends, APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from models import *
import database
import schemas
import os

router = APIRouter(
    prefix="/images",
    tags=['Images']
)

path = "/Users/aidarov/PycharmProjects/sdu_news/images"

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Image)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    file.filename = str(file.filename).replace(" ", "_")
    contents = await file.read()

    with open(f"{path}/{file.filename}", "wb") as f:
        f.write(contents)

    image = models.Image(path=file.filename)
    db.add(image)
    db.commit()
    db.refresh(image)

    return image

@router.get("/{filename}")
def get_images(filename: str):
    file_path = os.path.join(path, filename)

    if os.path.exists(file_path):
        return FileResponse(file_path)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File with {filename} name was not found")