from fastapi import FastAPI
from . import schema
import uvicorn
app = FastAPI()

@app.post('/blog')
def makePost(request:schema.blog):
    return {'name':{request.title},
            'body':{request.body}}

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=7000)