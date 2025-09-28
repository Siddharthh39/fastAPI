from pydantic import BaseModel

class blog(BaseModel):
    title : str
    body : str
    
    class Config:
        orm_mode = True


class User(BaseModel):
    name : str
    mail : str
    # password : str
    
    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    id: int
    body: str
    creator: User
     
    class Config:
        orm_mode = True