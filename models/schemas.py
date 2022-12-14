from typing import Set, Union, List
from pydantic import BaseModel

class LandlordAddressSchema(BaseModel):
    streetNumber: str
    streetName: str
    city: str
    province: str
    postalCode: str
    unitNumber: str
    poBox: str

class LandlordSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    state: str
    deviceId: str
    profileURL: str
    password: str
    landlordAddress: Union[LandlordAddressSchema, None]
  
class CreateLandlordSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    password: str
    landlordAddress: Union[LandlordAddressSchema, None]

class LoginSchema(BaseModel):
    email: str
    password: str
    deviceId: str
