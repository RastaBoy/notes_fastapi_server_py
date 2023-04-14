from pydantic import BaseModel, EmailStr

class AuthorizationRequest(BaseModel):
    email : EmailStr
    password : str