from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import database, schemas, models, utils, oatch2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['Authentication'])

@router.post('/login', status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = (db.query(models.User).filter(models.User.email == user_credential.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = oatch2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

