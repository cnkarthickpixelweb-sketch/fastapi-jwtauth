from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import JWT_SECRECT_KEY,JWT_ALGORITHM,JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException,status,Depends



security = HTTPBearer()

## JWT CREADENTILAS
SECRET_KEY = JWT_SECRECT_KEY   
ALGORITHM = JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = JWT_ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

## GENERATE HASH PASSWORD
def generate_hash_password(password: str):
        return pwd_context.hash(password)


## VERIFY HASH PASSWORD
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


## CRATE ACCESS TOKEN JWT
def create_access_token(data:dict):

    if not SECRET_KEY:
        raise HTTPException(status_code=404, detail={
            'success' : False,
            'message' : 'Your Screctkey is missing'
        })
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


## VERIFY ACCESS TOKEN JWT
def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload.pop("exp", None)
        return payload   
    except JWTError:
        return HTTPException(status_code=404,detail={'sucess': False , 'message': 'Invaild Token'  })



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
