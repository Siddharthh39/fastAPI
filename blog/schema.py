from pydantic import BaseModel
from typing import List

class blogBase(BaseModel):
    title : str
    body : str
    
class blog(blogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name : str
    mail : str
    password : str

    
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    name : str
    mail : str
    posts : List[blog] = []
    
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import List, Optional

class blog(BaseModel):
    title : str
    body : str

class BlogBase(BaseModel):
    title: str
    body: str
    
    class Config:
        from_attributes = True

class User(BaseModel):
    name : str
    mail : str
    password : str

class UserResponse(BaseModel):
    id: int
    name: str
    mail: str
    blog: List[BlogBase] = []
    
    class Config:
        from_attributes = True

class ShowBlog(BaseModel):
    title: str
    id: int
    body: str
    creator: UserResponse
     
    class Config:
        from_attributes = True