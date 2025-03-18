from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.params import Body

from pydantic import BaseModel
from typing import Annotated

import uvicorn
import json
import random
import time
from loguru import logger

import psycopg2


## run this:
with open("config.json") as config_file:
    config = json.load(config_file)

host_vm = config["application"]["host"]
port_vm = config["application"]["port"]
vm_ip = config["vm"]["ip"]
password = config["vm"]["pass"]

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool | None = None
    rating: int | None = None

while True:
    try:
        conn = psycopg2.connect(host="localhost", 
                                database="mydatabase",
                                user="postgres",
                                password="password123",
                                port=5432,
                                # cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        logger.debug(f'Database connection successful.'),
        break
    except Exception as e:
        logger.debug(f'Database connection failed.')
        logger.debug(f'Error: {e}')
        time.sleep(2)


my_posts = [{
    "title": "title of post 1",
    "content": "content of post 1", 
    "id" : 1
    },
    {
    "title": "title of post 2",
    "content": "content of post 2", 
    "id" : 2
    }
]

# @app.get("/", include_in_schema=False)
# async def redirect_to_docs():
#     return RedirectResponse(url="/docs")

@app.get("/")
async def root():
    return {"message": "Hello World"}

## all posts
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    logger.debug(f"posts: {posts}")
    conn.commit()
    return {"n": len(posts), "data": posts}

@app.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts():
    cursor.execute(""" DELETE FROM posts""")
    conn.commit()
    Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES( %s, %s, %s)
                   RETURNING * """, (post.title, post.content, post.published) )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


## single post

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found.")
    conn.commit()
    return { "post_detail":  post }
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id, ))
    deleted_post = cursor.fetchone()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist.")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist.")
    conn.commit()
    return {"message": updated_post}


if __name__ == "__main__":
    uvicorn.run(app, host=host_vm, port=port_vm)
    ## OR
    ## >>> uvicorn main:app --host 172.25.13.145 --port 8080
