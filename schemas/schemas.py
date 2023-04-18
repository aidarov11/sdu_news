from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Image(BaseModel):
    id: int
    path: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    firebase_uid: str
    first_name: str
    last_name: str


class User(BaseModel):
    id: int
    firebase_uid: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    image_path: Optional[str] = None

    class Config:
        orm_mode = True


class CreateCategory(BaseModel):
    parent_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    image_id: Optional[int] = None


class Category(BaseModel):
    id: int
    parent_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None

    class Config:
        orm_mode = True


class CreateArticle(BaseModel):
    title: str
    description: str
    is_events: bool = False
    image_id: int
    category_id: int
    user_id: int


class Article(BaseModel):
    id: int
    title: str
    description: str
    likes: int
    views: int
    is_events: bool
    image_id: int
    category_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ArticleOut(BaseModel):
    id: int
    title: str
    description: str
    likes: int
    views: int
    is_events: bool
    image_path: str
    category_name: str
    user_first_name: str
    user_last_name: str
    comments_count: int
    created_at: datetime

    class Config:
        orm_mode = True


class CreateComment(BaseModel):
    parent_id: Optional[int] = None
    comment: str
    user_id: int
    article_id: int


class Comment(BaseModel):
    id: int
    parent_id: Optional[int] = None
    comment: str
    likes: int
    user_id: int
    article_id: int
    created_at: datetime

    class Config:
        orm_mode = True