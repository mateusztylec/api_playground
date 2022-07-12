#!/usr/bin/python
# -*- coding: utf-8 -*-
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional
from random import randrange
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='zenbook',
                                cursor_factory=RealDictCursor)  # RealDectCursor zwraca wartości bez kluczy z SQL czy cos takeigo
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Conncetion to database failes")
        print("Error", error)
        time.sleep(2)

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#             {"title": "favourite foods", "content": "I like pizza", "id": 2}]


@app.get("/")
async def root():
    return {"message": "how it's going"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

