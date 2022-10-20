from typing import Optional
from venv import create
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

#for posts
class PostBase(BaseModel):
    title: str     
    content: str   
    published: bool = True 

class CreatePost(PostBase):
    pass #will receive whatever is inside the postbase class

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode= True


#will be return to user
class Post(PostBase):#(BaseModel):
    id: int
    # title: str     
    # content: str   
    # published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut #will return userout datas as a nested dict
    class Config:
        orm_mode= True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode= True


#to create a user
class UserCreate(BaseModel):
    email: EmailStr #validates email address     
    password: str 


#to login
class UserLogin(BaseModel):
    email: EmailStr #validates email address     
    password: str 


class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)