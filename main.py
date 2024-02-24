from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, validator
import re

app = FastAPI()


class User(BaseModel):
    id : int = None
    username : str = Field(..., min_length=3, max_length=50)
    email : str = Field(..., pattern="[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+")
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



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/user")
async def create_user(user: User):
    return user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)