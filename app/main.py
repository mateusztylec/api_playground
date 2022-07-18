#!/usr/bin/python
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import Settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "how it's going"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
