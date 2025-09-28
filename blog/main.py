from fastapi import FastAPI
from .database import engine, base
from .routes import blog_router, user_router

app = FastAPI()
base.metadata.create_all(engine)

app.include_router(blog_router)
app.include_router(user_router)