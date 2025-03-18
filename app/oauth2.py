from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, models
from .database import get_db
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from loguru import logger
from .config import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # this is the endpoint to login url

settings = Settings()

SECRET_KEY = settings.secret_key # bash: openssl rand -hex 32
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # called like : data={"user_id": user.id}
    to_encode = data.copy() # safe copy

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id", None)

        if id is None:
            raise credentials_exceptions
        
        token_data = schemas.TokenData(id=id)

    except JWTError as e:
        logger.error(e)
        raise credentials_exceptions
    except AssertionError as e:
        logger.error(e)
    
    return token_data


# Main function to interact with access dependent operations
def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(get_db)) -> schemas.UserResponse:
    """ Query database, fetches the user. Gets called in path operations to handle auth verification."""
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"} 
    )

    token = verify_access_token(token=token, credentials_exceptions=credential_exceptions)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user