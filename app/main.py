from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import mysql.connector
import time
import config

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        connection = mysql.connector.connect(
            host= config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )

        cursor = connection.cursor()
        print("Database connection secured.")
        break
    except Exception as error:
        print("Database connection was failed: ", error)
        time.sleep(2)


def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index(id):
    for i in range(len(my_posts)):
        if my_posts[i]["id"] == id:
            return i
    return -1


@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    post_dict = [{"id": row[0], "title": row[1], "content": row[2]}
                 for row in posts]
    print(post_dict)
    return {"data": post_dict}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """ INSERT INTO fastapi.posts (title, content) VALUES (%s,%s) """, (post.title, post.content))
    connection.commit()
    return {"message": "Post was successful!"}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    try:
        cursor.execute(""" SELECT * from posts WHERE id = %s """, (id,))
        post = cursor.fetchone()
        if post:
            post_dict = {"id": post[0], "title": post[1], "content": post[2]}
            return {"data": post_dict}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Post not found!"}
    except Exception as error:
        print("Error occurred: ", error)
        return {"message": error}


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        cursor.execute(
            """ DELETE FROM posts WHERE id = %s """, (id, ))
        connection.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as error:
        print("Error occurred: ", error)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.put("/post/{id}")
def update_post(id: int, post: Post):
    try:
        cursor.execute(""" UPDATE posts SET title = %s , content = %s , created_at = NOW() WHERE id = %s RETURNING * """,
                       (post.title, post.content, id))
        new_post = cursor.fetchone()
        if new_post:
            connection.commit()
            return {"message": "Post Updated"}
    except Exception as error:
        print("Error occured: error")
        return {"message": error}
