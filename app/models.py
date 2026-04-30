from pydantic import BaseModel

class ConverterInput(BaseModel):
    vin: float
    duty: float

class UserLogin(BaseModel):
    username: str
    password: str
    