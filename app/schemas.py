from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# This class is to create a schema for users
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# This is to shape the response to the user once the user is created
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# This class is to control the response to the user
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


# This is to shape the user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# This is going to have the schema for the Token once the user is logged in

class Token(BaseModel):
    access_token: str
    token_type: str


# We also have a schema for the Token Data that will be stored

class TokenData(BaseModel):
    id: Optional[str] = None


# Schema for Votes

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


# This class is to control the response to the user + returning a JOINT statement to include votes/likes
class PostOut(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True


