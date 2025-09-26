from fastapi import FastAPI
from . import schema

app = FastAPI()

@app.post('/blog')
def makePost(request:schema.blog):
    return request