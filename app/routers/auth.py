from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserLogin
from ..models import User
from .. import utils, oauth2, schemas

from loguru import logger
router = APIRouter(
    tags = ["AUTHENTICATION"]
)

@router.post("/login", response_model=schemas.Token)
def login( user_credentials: OAuth2PasswordRequestForm= Depends(),
           db: Session = Depends(get_db)
    ):
    # user_credentials keys: username, password
    # expects request in form-data (NOT json)
    user = db.query(User).filter(User.email == user_credentials.username).first() # database stored

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials.")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials.")
    
    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id}) # arbitrary payload content
    logger.debug(f'access_token created')

    return {"access_token": access_token, 
            "token_type": "Bearer Token"}
