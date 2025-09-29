from fastapi import APIRouter, HTTPException, status, Depends
from .. import schema, models, database, hashing, jwtToken
from .. database import get_db
from sqlalchemy.orm import Session
from datetime import timedelta
from ..jwtToken import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..hashing import Hashing
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Auth"],
)

@router.post('/login', response_model=schema.Token)
def loginUser(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
    
    access_token = create_access_token(data={"sub": user.mail})
    return schema.Token(access_token=access_token, token_type="bearer")
    

 