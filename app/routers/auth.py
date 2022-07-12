from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import database, schemas, models, utils, oatch2
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])

@router.post('/login', status_code=status.HTTP_201_CREATED)
def login(user_credential: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = (db.query(models.User).filter(models.User.email == user_credential.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    access_token = oatch2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

