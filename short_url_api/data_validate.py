from pydantic import BaseModel

class user(BaseModel):
    username:str
    password:str

class shorturl(BaseModel):
    url :str
    shortend:str

class update_url(BaseModel):
    url:str
    shortend:str
    updated_at :str
