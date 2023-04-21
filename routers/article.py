from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
import database
import models
import schemas

router = APIRouter(
    prefix="/articles",
    tags=["Article"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Article)
def create_article(article: schemas.CreateArticle, db: Session = Depends(database.get_db)):
    new_article = models.Article(**article.dict())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


@router.get("/{article_id}", response_model=schemas.ArticleOut)
def get_article_by_id(article_id: int, db: Session = Depends(database.get_db)):
    subq = db.query(
        models.Comment.article_id,
        func.count(models.Comment.id).label("comments_count")
    ).group_by(models.Comment.article_id).subquery()

    article = db.query(
        models.Article.id,
        models.Article.title,
        models.Article.description,
        models.Article.likes,
        models.Article.views,
        models.Article.is_events,
        models.Image.path.label("image_path"),
        models.Category.name.label("category_name"),
        models.User.first_name.label("user_first_name"),
        models.User.last_name.label("user_last_name"),
        subq.c.comments_count,
        models.Article.created_at
    ).select_from(models.Article).join(
        models.Image,
        onclause=models.Image.id == models.Article.image_id
    ).join(
        models.Category,
        onclause=models.Article.category_id == models.Category.id
    ).join(
        models.User,
        onclause=models.Article.user_id == models.User.id
    ).join(
        subq,
        onclause=models.Article.id == subq.c.article_id
    ).filter(
        models.Article.id == article_id
    ).first()

    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id {article_id} not found")

    return article


@router.get("/", response_model=List[schemas.ArticleOut])
def get_articles(db: Session = Depends(database.get_db)):
    subq = db.query(
        models.Comment.article_id,
        func.count(models.Comment.id).label("comments_count")
    ).group_by(models.Comment.article_id).subquery()

    article = db.query(
        models.Article.id,
        models.Article.title,
        models.Article.description,
        models.Article.likes,
        models.Article.views,
        models.Article.is_events,
        models.Image.path.label("image_path"),
        models.Category.name.label("category_name"),
        models.User.first_name.label("user_first_name"),
        models.User.last_name.label("user_last_name"),
        subq.c.comments_count,
        models.Article.created_at
    ).select_from(models.Article).join(
        models.Image,
        onclause=models.Image.id == models.Article.image_id
    ).join(
        models.Category,
        onclause=models.Article.category_id == models.Category.id
    ).join(
        models.User,
        onclause=models.Article.user_id == models.User.id
    ).join(
        subq,
        onclause=models.Article.id == subq.c.article_id
    ).all()

    # filter
    # tranding views
    # hot likes
    # faculty, clubs id
    # events false

    if article == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Articles empty")

    return article


@router.post("/like")
def increase_article_like(article_id: int, db: Session = Depends(database.get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).update({'likes': models.Article.likes + 1})
    db.commit()

    if article:
        return Response(status_code=status.HTTP_202_ACCEPTED)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id {article_id} not found")