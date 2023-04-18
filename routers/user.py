from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
import database
import schemas

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

# Upload user image

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.CreateUser, db: Session = Depends(database.get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User.id, models.User.firebase_uid, models.User.first_name, models.User.last_name, models.User.phone_number, models.Image.path).join(models.Image).filter(models.User.id == user_id).first()

    if user is None:
        user = db.query(models.User).filter(models.User.id == user_id).first()
    else:
        user = schemas.User(id=user[0], firebase_uid=user[1], first_name=user[2], last_name=user[3], phone_number=user[4], image_path=user[5])

    check_if_exists(user, user_id)
    return user


def check_if_exists(user, user_id):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id}  was not found")


# @router.put("/{user_id}", response_model=schemas.User)
# def update_user(user_id: int, user: schemas.CreateUser, db: Session = Depends(database.get_db)):
#     user_query = db.query(models.User).filter(models.User.id == user_id)
#     found_user = user_query.first()
#
#     check_if_exists(found_user, user_id)
#     user_query.update(user.dict(), synchronize_session=False)
#     db.commit()
#
#     return user_query.first()