from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from fastapi import Body
#from pydantic import BaseModel
#from random import randrange
#from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user, auth

from .config import settings

#models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# This means only google domain will be able to use your api .
# origins = ["https://www.google.com"]
#below is for all domain or website. This means anybody can use our api, its public. 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_posts = [{"title": "title of post 1", "content":"content of post 1", "id": 1}, {"title": "favourite food", "content":"Ilike pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api!!"}



