from fastapi import APIRouter, status, Depends, HTTPException
from typing import Union, List
from sqlalchemy.orm import Session
import database
import models
import schemas

router = APIRouter(
    prefix="/categories",
    tags=['Category']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Category)
def create_category(category: schemas.CreateCategory, db: Session = Depends(database.get_db)):
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=List[schemas.Category])
def get_categories(parent_id: Union[int, None] = None, db: Session = Depends(database.get_db)):
    if parent_id:
        categories = db.query(models.Category.id, models.Category.parent_id, models.Category.name, models.Category.description, models.Image.path.label("image_path")).join(models.Image, isouter=True).filter(models.Category.parent_id == parent_id).all()

        if categories == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categories with parent_id {parent_id} was not found")
    else:
        categories = db.query(models.Category.id, models.Category.parent_id, models.Category.name, models.Category.description, models.Image.path.label("image_path")).join(models.Image, isouter=True).all()

        if categories == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categories empty")

    return categories


@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(database.get_db)):
    category = db.query(models.Category.id, models.Category.parent_id, models.Category.name, models.Category.description, models.Image.path.label("image_path")).join(models.Image, isouter=True).filter(models.Category.id == category_id).first()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} was not found")

    return category




