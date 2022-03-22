from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


# THE FOLLLOWING DECORATORS ARE USING SQL LANGUAGE

#This decorators use the @ symbol to be able to use a http command.
#We are also telling the server what to "get" from the root page
@app.get("/")
async def root():
    return {"message": "Welcome to JexMo Enterprise API"}

#Creating a new page for posts, still using the .get command.
@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts_table""")
    posts = cursor.fetchall()
    return {"data": posts}

#Creating a POST request
@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(payload: schemas.PostCreate):
    #payload is where we are going to store whatever is received from the sender
    cursor.execute("""INSERT INTO posts_table (title, content, published) VALUES (%s, %s, %s)""", (payload.title, payload.content, payload.published))
    con.commit()
    #message returned to the user
    cursor.execute("""SELECT * FROM posts_table WHERE created_column = (SELECT MAX(created_column) FROM posts_table)""")
    latest_post = cursor.fetchone()
    return{'data': latest_post}

#This next path/decorator is going to be used to retreive a post based on its id
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts_table WHERE id_post = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found')
    return {"post_detail": post}
#Creating a DELETE request
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #This is to return the information on the post that was deleted
    cursor.execute("""SELECT * FROM posts_table WHERE id_post = %s""", (str(id)))
    deleted_post = cursor.fetchone()

    #This section is to actually delete the requested post
    cursor.execute("""DELETE FROM posts_table WHERE id_post = %s""", (str(id)))
    con.commit()
    if deleted_post is not None:
        return {'deleted post': deleted_post}

    #This is to return an error message if needed
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with {id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Creating a UPDATE request
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate):
    #Query to update post
    cursor.execute("""UPDATE posts_table SET title = %s, content = %s, published = %s WHERE id_post = %s""", (post.title, post.content, post.published, str(id)))
    con.commit()

    #Query to return the updated post
    cursor.execute("""SELECT * FROM posts_table WHERE id_post = %s""", (str(id)))
    updated_post = cursor.fetchone()
    if updated_post is not None:
        return {'Updated post': updated_post}
    #This is to return an error message if needed
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with {id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)