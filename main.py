from fastapi import FastAPI, Request, HTTPException, Depends, Response, Cookie
from pydantic import BaseModel, Field, validator, EmailStr
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
import re
import secrets
import json

app = FastAPI()

USERNAME = "admin"
PASSWORD = "password"
SESSION_COOKIE_NAME = "session"

session_db = {}
class User(BaseModel):
    id : int = None
    username : str = Field(..., min_length=3, max_length=50)
    email : EmailStr
    image_file : str = None
    name : str = None
    password : str = None

    @validator("username")
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('debe ser alfanumerico')
        return v

    @validator("name")
    def name_alphanumeric(cls, v):
        pattern = r"^[a-zA-Z ]+$"
        if not re.match(pattern, v):
            raise ValueError('debe contener unicamente letras y espacios')
        return v

class SessionData(BaseModel):
    username: str


def generate_session_token():
    return secrets.token_hex(16)

def create_session(username: str):
    session_token = generate_session_token()
    session_db[session_token] = SessionData(username=username)
    return session_token

def get_session(session_token: str):
    print(session_db)
    print(session_token)
    return session_db.get(session_token)

def get_current_session(session_token: str = Cookie(None)):
    session_data = get_session(session_token)
    if session_data is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    return session_data

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/user")
async def create_user(user: User):
    return user


def check_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    correct_username = credentials.username == USERNAME
    correct_password = credentials.password == PASSWORD
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True



@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    if check_auth(credentials):
        # Generamos un session para el usuario
        session_token = create_session(credentials.username)
        response_content= {"message": "Login successful"}
        response = Response(content=json.dumps(response_content))
        response.set_cookie(key = SESSION_COOKIE_NAME, value=session_token)
        return response
    else:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

@app.get("/secure")
async def secure_endpoint(session_data: SessionData = Depends(get_current_session)):
    return JSONResponse(content={"message": "Secure content"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)