from sqlalchemy.orm import Session
from .. import models, schema
from ..hashing import Hashing
from fastapi import HTTPException, status


def create_user(request: schema.User, db: Session) -> models.User:
    """Create a new user"""
    newUser = models.User(
        name=request.name,
        mail=request.mail,
        password=Hashing().hashPassword(request.password)
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


def get_user_by_id(id: int, db: Session) -> models.User:
    """Get a user by ID"""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no user with id {id} found"
        )
    return user
