from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schema, models
from .database import engine, base, localSession
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hashing


app = FastAPI()
base.metadata.create_all(engine)

def get_db():
    db = localSession()
    try:
        yield db
    
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schema.ShowBlog, tags=["Blogs"])
def makePost(request:schema.blog, db : Session = Depends(get_db), user_id:int = 1):
    newPost = models.Blog(title = request.title, body = request.body, user_id=user_id)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@app.get('/blog', response_model=List[schema.ShowBlog], tags=["Blogs"])
def showAllBlogs(db : Session = Depends(get_db), user_id:int = 1):
    blogs = db.query(models.Blog).filter(models.Blog.user_id == user_id).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schema.ShowBlog, tags=["Blogs"])
def getBlogId(id:int, response:Response,db : Session = Depends(get_db), user_id:int = 1):
    returnId = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user_id == user_id).first()
    if not returnId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'no blog for id {id} found')
    return returnId

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def deletblog(id:int, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"not blog to delete with id {id}")
    
    blog.delete(synchronize_session=False)
    db.commit()

    return "done"

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def updateBlog(id:int, request:schema.blog, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no blog to update with id {id}")
    
    blog.update(request.dict(), synchronize_session=False)
    db.commit()
    return "updated"



@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schema.User, tags=["Users"])
def createUser(request:schema.User, db : Session = Depends(get_db)):
    newUser = models.User(name = request.name, mail = request.mail,
                          password = Hashing().hashPassword(request.password))
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@app.get('/user/{id}', response_model=schema.User, tags=["Users"])
def getUser(id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no user with id {id} found")
    return user