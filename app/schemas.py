from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

## USER -----------------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
## -----------------------------------------
## TOKENS  ---------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None

## -----------------------------------------
## POSTS  ----------------------------------
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes = True
## -------------------------------------------
## VOTE --------------------------------------
class Vote(BaseModel):
    post_id: int
    dir: int = Field(ge=0, le=1) # constrained integer: metto like, tolgo like

