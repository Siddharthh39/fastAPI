from fastapi import APIRouter, Depends, status, Response
from .. import schema
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..repository import blog as blog_repository

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.ShowBlog)
def makePost(request: schema.blog, db: Session = Depends(get_db), user_id: int = 1):
    return blog_repository.create_blog(request, db, user_id)

@router.get('/', response_model=List[schema.ShowBlog])
def showAllBlogs(db: Session = Depends(get_db)):
    return blog_repository.get_all_blogs(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.ShowBlog)
def getBlogId(id: int, response: Response, db: Session = Depends(get_db)):
    return blog_repository.get_blog_by_id(id, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletblog(id: int, db: Session = Depends(get_db)):
    return blog_repository.delete_blog(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id: int, request: schema.blog, db: Session = Depends(get_db)):
    return blog_repository.update_blog(id, request, db)
