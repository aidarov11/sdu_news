from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import database
import models
import schemas

router = APIRouter(
    prefix="/comments",
    tags=["Comment"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
def create_comment(comment: schemas.CreateComment,db: Session = Depends(database.get_db)):
    new_comment = models.Comment(**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get("/{article_id}", response_model=List[schemas.Comment])
def create_comment(article_id: int, db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).filter(models.Comment.article_id == article_id).all()

    if comments == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comments with article_id {article_id} not found")

    return comments