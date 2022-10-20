#uvicorn main:app --reload 
#uvicorn app.main:app --reload
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#without alembic
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#"*" will allow your api to be accessed anywhere, but you can add strict specificity like, "yoursite.com"
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts =[{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
#  {'title': 'favorite food', 'content': 'I like pizza', 'id': 2}]
# #print(my_posts[-1]['id']+1)

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

#for posts specifict routes
app.include_router(post.router)
#for users specifict routes
app.include_router(user.router)
#for password authentications
app.include_router(auth.router)
#for user vote
app.include_router(vote.router)

@app.get("/")
def root():
    return{"message": "Welcome to my api"}