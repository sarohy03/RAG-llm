from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
import os
from dotenv import load_dotenv
from Config import user_collection, bot_collection
from LLaMa import response_gen
from Embedding import relevent_data

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class UserProfile(BaseModel):
    username: str



class SignupRequest(BaseModel):
    username: str
    password: str

# MongoDB utility functions
def get_user_by_username(username: str):
    return user_collection.find_one({"clientname": username})

def create_user(username: str, hashed_password: str):
    user = {
        "clientname": username,
        "hashed_pass": hashed_password,
    }
    result = user_collection.insert_one(user)
    return result

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    user_data = {
        "username": user["clientname"],
        "hashed_password": user["hashed_pass"],
    }
    user_in_db = UserInDB(**user_data)
    if not verify_password(password, user_in_db.hashed_password):
        return False
    return user_in_db

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    user_data = {
        "username": user["clientname"],
        "hashed_password": user["hashed_pass"],
    }
    return UserInDB(**user_data)

@router.post("/login-user", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup-user")
def signup(signup_request: SignupRequest):
    existing_user = get_user_by_username(signup_request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = pwd_context.hash(signup_request.password)
    create_user(signup_request.username, hashed_password)
    return {"message": "User created successfully"}

@router.get("/profile-user", response_model=UserProfile)
async def get_user_profile(current_user: UserInDB = Depends(get_current_user)):
    user_profile = {
        "username": current_user.username
    }
    return user_profile


class Query(BaseModel):
    command: str

@router.get("/useBot/{id}")
async def create_bot(query: Query, id: int, current_user: UserInDB = Depends(get_current_user) ):
    result = bot_collection.find_one({"id": id})
    if result is None:
        return {"result": "bot not found"}

    acha_result = relevent_data(query.command , result["context"])
    print(acha_result)
    r = await response_gen(acha_result, query.command)
    return {"result": r}
