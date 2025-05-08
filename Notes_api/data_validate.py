from pydantic import BaseModel

class signup(BaseModel):
    username : str
    password : str

class Notes(BaseModel):
    title : str
    description : str


