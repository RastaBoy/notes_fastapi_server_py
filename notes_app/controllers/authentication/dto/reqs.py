from pydantic import BaseModel, EmailStr

class AuthRequest(BaseModel):
    email : EmailStr
    password : str


class RegisterRequest(BaseModel):
    email : EmailStr
    first_name : str
    second_name : str
    password : str
    