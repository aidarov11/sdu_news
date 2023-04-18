from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

# Todo
# ondelete Cascade

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    firebase_uid = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    image_id = Column(Integer, ForeignKey("images.id"))

    image = relationship("Image", back_populates="user")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    views = Column(Integer, default=0, nullable=False)
    is_events = Column(Boolean, default=False, nullable=False)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    image = relationship("Image", back_populates="article")
    category = relationship("Category")
    user = relationship("User")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    parent_id = Column(Integer)
    comment = Column(String, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User")
    article = relationship("Article")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, nullable=False)
    path = Column(String, nullable=False)

    user = relationship("User", uselist=False, back_populates="image")
    category = relationship("Category", uselist=False, back_populates="image")
    article = relationship("Article", uselist=False, back_populates="image")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    parent_id = Column(Integer)
    name = Column(String, nullable=False)
    description = Column(String)
    image_id = Column(Integer, ForeignKey("images.id"))

    image = relationship("Image", back_populates="category")


# alembic init migrations
# alembic revision --autogenerate -m "DataBase creation"
# alembic upgrade 42ce66f6118b




