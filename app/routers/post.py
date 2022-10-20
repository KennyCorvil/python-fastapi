from pyexpat import model
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func #to get access to thew funtion count
from app import oauth2
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

#will add "posts" to all the request links
router = APIRouter(prefix="/posts", tags=["Posts"])#the tags is used to customize the documentations for /docs


#get all posts
#@router.get("/", response_model=list[schemas.Post])#no votes data
@router.get("/", response_model=list[schemas.PostOut])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):#without query parameters
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
 skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #posts result without votes
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #sqlalchememy by default uses INNER JOIN whereas raw sql statements default to OUTER JOIN when you only type LEFT JOIN
    posts =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #to make sure only the user who made the posts can retreave them
    # posts = db.query(models.Post).filter(models.Post.owner_id == int(current_user.id)).all()
    #print(posts)
    return posts

#create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):#makes sure the user is login before they can create a post
    # post_dict = post.dict()
    # post_dict['id'] = my_posts[-1]['id']+1
    # #.dict() converts the data into a dictionary
    # my_posts.append(post_dict)
    # #%s reprensent a variable to be passed like in c
    #without sqlalchemy
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    # (post.title, post.content, post.published))
    #directly passing the data in a f string ie.
    # (f"INSERT INTO posts (title, content, published VALUE (post.title, post.content, post.published)")
    #is vulnerable to attack such as sql injections
    # new_post = cursor.fetchone()
    #commit to finally save it to the database
    # conn.commit()

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #better yet, turn post into a dictionary and past it with pointers
    
    
    # new_post = post.dict()
    
    # new_post["owner_id"] = int(current_user.dict()["id"])
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#work as a RETURNING sql statement
    return new_post

#search by id
@router.get("/{id}", response_model=schemas.PostOut)#{id} is the path parameter
def get_post(id: int, response: Response, db: Session = Depends(get_db)):#will automatically convert id into an int
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    
    # post = find_post(int(id))
    # post = find_post(id)
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first() #no votes

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f'post with the id {id} was not found'}
        #better. raise exeption
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with the id {id} was not found')
    return post

#delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):#makes sure the user is login before they can delete a post
    #find index
    #index = find_index_post(id)

    #without sqlalchemy
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # print(delete_post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # print(post.owner_id, type(post.owner_id))
    # print(current_user.id, type(current_user.id))
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with the id {id} was not found')
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to performe requested action')
    
    post_query.delete(synchronize_session=False)
    db.commit()
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)#not supposed to return any data back

#update post using put
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):#makes sure the user is login before they can update a post
    #without sqlalchemy
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #  (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    #index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with the id {id} was not found')
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to performe requested action')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post_query.first()