from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# openssl rand -hex 32
SECRET_KEY = "9ff4d6ebe6653647073d4f5f87aae22903a230e3b6055baf03fcf2d7209e934e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


db = {
    "naga" : {
        "username" : "naga",
        "full_name" : "naga",
        "email" : "naga@gmail.com",

        "hashed_password" : "$2b$12$BAu3De.CFOPlWrduExQjWuEw5Z.d.qQEM9.7ikujQ8HkdlFVz9aU6"
    }
}

class User(BaseModel):
    username: str
    full_name : str or None = None
    email : str or None = None


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : str or None = None

class UserInDb(User):
    hashed_password : str or None = None

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto" )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username : str):
    if username in db:
        user_data = db[username]
        return UserInDb(**user_data)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if username not in db:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data : dict, expires_delta : timedelta or None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    #to_encode.update("exp", expire)
    encoded_jwt = jwt.encode(to_encode, key = SECRET_KEY, algorithm=ALGORITHM )
    return encoded_jwt

async def get_current_user(token : str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Could not validate credential 2",
                             headers={"WWW-Authenticate" : "Bearer"})
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])

        username : str = payload.get("subs")
        if username is None:
            raise credential_exception

        token_data = TokenData(username = username)

    except JWTError:
        raise credential_exception

    user = get_user(db, username = token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user : UserInDb = Depends(get_current_user)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends()):
    print("inside login_for_access")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password 1",
                            headers={"WWW-Authenticate" : "Bearer"})
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"subs" : user.username} , expires_delta=access_token_expires)
    print(f"access_token {access_token} generated")
    return {"access_token" : access_token , "token_type" : "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user :User = Depends(get_current_active_user)):
    return current_user

#phash = get_password_hash("naga1234")
#print(phash)