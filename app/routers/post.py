from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func

# This is to activate the routers
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# THIS DECORATORS ARE USING SQL ALCHEMY

# This function is to get all posts using strictly sqlalchemy
@router.get("/", response_model=List[schemas.PostOut])
def get_post_alchemy(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    results = db.query(
        models.Post, func.count(models.Vote.post_id).label("likes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id) \
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


# This function creates a post using alchemy
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post_alchemy(post: schemas.PostCreate, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,
                           **post.dict())  # we used **post.dict to unpack all variables in our model compare this line to line 77 where
    # you have to use payload.title, payload.content etc.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# This function is to look up a post by id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post_alchemy(id: int, db: Session = Depends(get_db)):
    post_by_id = db.query(
        models.Post, func.count(models.Vote.post_id).label("likes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id) \
        .group_by(models.Post.id).first()
    if not post_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found')
    return post_by_id


# This function is to delete a post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_alchemy(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    # This if statement is to make sure users only delete their own posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# This function is to update a current post using sqlalchemy
@router.put("/{id}", response_model=schemas.Post)
def update_posts_alchemy(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                         current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    xpost = post_query.first()
    if xpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with {id} does not exist')
    if xpost.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perfom requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
