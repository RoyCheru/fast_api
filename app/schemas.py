from pydantic import BaseModel,EmailStr, conint, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

#below is a schema/pydantic model. It defines the structure of a requests and response
#it ensure that when a user wants to create a post, the request will only go through if it has a 'title' and 'content' in the body
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    

#from here we define how response should be. We want those fields to be send back to user when he i.e creates a post
#the other field I have inherited from postbase to avoid repetition
class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        

class Post(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]