from dataclasses import dataclass

@dataclass
class AuthRequest:
    email : str
    password : str


class RegisterRequest:
    email : str
    first_name : str
    second_name : str
    password : str
    