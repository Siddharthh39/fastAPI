from fastapi import APIRouter, HTTPException, status, Depends
from .. import schema, models, database, hashing
from .. database import get_db
from sqlalchemy.orm import Session

from ..hashing import Hashing

router = APIRouter(
    tags=["Auth"],
)

@router.post('/login')
def loginUser(request: schema.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.mail == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )
    hashing_instance = Hashing()

    if not hashing_instance.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"invalid password"
        )
    
    return user

