from jose import JWTError, jwt
from datetime import datetime, timedelta

#SECRET_KEY
#ALGORITHM
#Expiration time

SECRET_KEY = "f78147da37181f1648883e56c32d2fdd94cf7362f9f3c92d1649fcb8fac01118"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


