from pydantic import BaseModel  



class User(BaseModel):
    name:str
    email:str
    password:str

class Show_user(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True

class Blog(BaseModel):
    title:str
    body:str

class Show_blog(BaseModel):
    title:str
    creator:Show_user
    body:str
    class Config():
        orm_mode = True