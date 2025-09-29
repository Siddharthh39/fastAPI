from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from . import jwtToken, schema, models
from .database import get_db
from sqlalchemy.orm import Session
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = jwtToken.verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.mail == token_data.mail).first()
    if user is None:
        raise credentials_exception
    
    return user
