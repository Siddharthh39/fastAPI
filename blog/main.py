from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schema, models
import uvicorn
from .database import engine, base, localSession
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()
base.metadata.create_all(engine)

def get_db():
    db = localSession()
    try:
        yield db
    
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schema.ShowBlog)
def makePost(request:schema.blog, db : Session = Depends(get_db)):
    newPost = models.Blog(title = request.title, body = request.body)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@app.get('/blog', response_model=List[schema.ShowBlog])
def showAllBlogs(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schema.ShowBlog)
def getBlogId(id:int, response:Response,db : Session = Depends(get_db)):
    returnId = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not returnId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'no blog for id {id} found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'detail':f'no blog for id {id}'}
    return returnId

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletblog(id:int, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"not blog to delete with id {id}")
    
    blog.delete(synchronize_session=False)
    db.commit()

    return "done"

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id:int, request:schema.blog, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no blog to update with id {id}")
    
    blog.update(request.dict(), synchronize_session=False)
    db.commit()
    return "updated"

@app.post('/user')
def createUser(request:schema.User, db : Session = Depends(get_db)):
    newUser = models.User(name = request.name, email = request.mail,
                          password = request.password)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser