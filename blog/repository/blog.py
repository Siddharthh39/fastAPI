from sqlalchemy.orm import Session
from .. import models, schema
from fastapi import HTTPException, status
from typing import List


def create_blog(request: schema.blog, db: Session, user_id: int) -> models.Blog:
    """Create a new blog post"""
    newPost = models.Blog(title=request.title, body=request.body, user_id=user_id)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


def get_all_blogs(db: Session) -> List[models.Blog]:
    """Get all blog posts"""
    blogs = db.query(models.Blog).all()
    return blogs


def get_blog_by_id(id: int, db: Session) -> models.Blog:
    """Get a blog post by ID"""
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'no blog for id {id} found'
        )
    return blog


def delete_blog(id: int, db: Session):
    """Delete a blog post by ID"""
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no blog to delete with id {id}"
        )
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {"message": "Blog deleted successfully"}


def update_blog(id: int, request: schema.blog, db: Session):
    """Update a blog post by ID"""
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no blog to update with id {id}"
        )
    
    blog.update(request.dict(), synchronize_session=False)
    db.commit()
    return {"message": "Blog updated successfully"}
