from fastapi import FastAPI
from routers import image, user, category, article, comment

app = FastAPI(
    title="SDU News",
    version="0.0.1",
    contact={
        "name": "Aidarov Alibek"
    },
    docs_url="/",
    redoc_url=None
)

app.include_router(image.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(article.router)
app.include_router(comment.router)