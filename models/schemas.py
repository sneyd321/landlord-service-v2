from typing import Set, Union, List
from pydantic import BaseModel


class CreateLandlordSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
  
class LoginSchema(BaseModel):
    email: str
    password: str
    deviceId: str
