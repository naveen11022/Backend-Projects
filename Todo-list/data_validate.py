from pydantic import BaseModel

class signup(BaseModel):
    username : str
    password : str

class todo(BaseModel):
    title : str
    description: str
    