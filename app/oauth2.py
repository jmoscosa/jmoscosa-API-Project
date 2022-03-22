from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret Key
SECRET_KEY = settings.secret_key
# Algorithm we will use
ALGORITHM = settings.algorithm
# Expiration time of token
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# Here we create the access token function
def create_access_token(data: dict):
    # We created a copy of the data to leave the original untouched
    to_encode = data.copy()
    # Here we are setting the expiration field
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Adding the expiration to the data
    to_encode.update({"exp": expire})

    # Here is where we are going to create the JWT token with the fields we have above.
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


# This function is going to verify the access token provided is the right one

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


# This function is going to track the token to verify the requested action is valid

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials"
                                          , headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
