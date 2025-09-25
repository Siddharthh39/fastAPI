from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def idx():
    return {'data':"blog List"}

@app.get('/blog/{id}')
def about(id:int):
    return {'data':(id)}

@app.get('/blog/{id}/comments')
def comment(id):
    return {'data':{'comments':{id}}}