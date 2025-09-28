from fastapi import APIRouter, Depends, status
from .. import schema
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import user as user_repository

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def createUser(request: schema.User, db: Session = Depends(get_db)):
    return user_repository.create_user(request, db)

@router.get('/{id}', response_model=schema.UserResponse)
def getUser(id: int, db: Session = Depends(get_db)):
    return user_repository.get_user_by_id(id, db)