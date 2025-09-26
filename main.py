from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, time
import uvicorn

app = FastAPI()

@app.get('/')
def idx():
    return {'data':"blog List"}

@app.get('/blog')
def checkblogs(limit:int=10, published:bool=True, sort:Optional[str] = None):
    if published:
        return{'data': f"{limit} are published blogs"}
    else:
        return{'data': 'published'}


@app.get('/blog/{id}')
def about(id:int):
    return {'data':(id)}

@app.get('/blog/{id}/comments')
def comment(id):
    return {'data':{'comments':{id}}}

class BlogTake(BaseModel):
    title : str
    datePosted : date = Field(default_factory=date.today)
    body : str

@app.post('/blog')
def postBlog(blog:BlogTake):
    return{'data':f'title of this blog is {blog.title} date is {blog.datePosted}'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)