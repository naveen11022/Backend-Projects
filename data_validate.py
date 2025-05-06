from pydantic import BaseModel

class signup(BaseModel):
    username : str
    password : str

class blogger(BaseModel):
    title : str
    content : str
    category : str
    tags : str