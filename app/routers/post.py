
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from loguru import logger

from ..database import get_db 
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ["POSTS"]

)

## all posts -------------------------------------------------
@router.get("/", response_model=list[schemas.PostResponse])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), 
              current_user: schemas.UserResponse = Depends(oauth2.get_current_user), 
              limit: int = 10,
              skip: int = 0, 
              search: str = ""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    logger.debug(f"#posts: {len(posts)}")
    logger.debug(f"posts: {type ( posts ) }")


    # counting upvotes
    # .join does left inner join by default. isouter=True to override
    results = db.query(
            models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.title.contains(search)
        ).limit(
            limit=limit
        ).offset(
            offset=skip
        ).all()
    logger.debug(f"results: {results}")
    out = [schemas.PostResponse(Post=post, votes=votes) for post, votes in results]

    return out



@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(db: Session = Depends(get_db)):
    db.query(models.Post).delete() # no filtering applied -> this matches the whole table
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts( post: schemas.PostBase,
                  db: Session = Depends(get_db),
                  response_model=schemas.Post, 
                  current_user: schemas.UserResponse = Depends(oauth2.get_current_user)
                  ):
    
    post_dict = post.model_dump()
    new_post = models.Post(owner_id = current_user.id, **post_dict)
    logger.debug(f'current_user: {current_user.email} created post {new_post.id}')


    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


## single post -------------------------------------------------

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, response: Response,
             db: Session = Depends(get_db),
             current_user: schemas.UserResponse = Depends(oauth2.get_current_user)
    ):

    post = db.query(
            models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.id == id
        ).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found.")
    return post
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post( id: int, db: Session = Depends(get_db),
                 current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post_to_delete = post_query.first()

    if post_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist.")
    
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform operation.")

    post_query.delete(synchronize_session=False)  # session is reset anyway after commit

    db.commit()
    logger.info(f'post {id} successfully deleted.')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, 
                db: Session = Depends(get_db),
                current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post_to_update = post_query.first()
    
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist.")
    
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform operation.")
    
    post_query.update(post.model_dump())
    db.commit()
    return post_query.first()