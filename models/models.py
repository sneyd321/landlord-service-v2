
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Landlord(Base):
    __tablename__ = 'landlord'

    id = Column(Integer(), primary_key=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    phoneNumber = Column(String(20), nullable=True)
    state = Column(String(50),  nullable=False)
    password = Column(String(255), nullable=False)
    deviceId = Column(String(180), nullable=True)
    profileURL = Column(String(223), nullable=True)
    landlordAddress = relationship("LandlordAddress", lazy="joined", backref="landlord", uselist=False)

    def __init__(self, **kwargs):
        self.firstName = kwargs.get("firstName")
        self.lastName = kwargs.get("lastName")
        self.email = kwargs.get("email")
        self.phoneNumber = kwargs.get("phoneNumber")
        self.state = "MFA_VALID"
        self.password = self.get_password_hash(kwargs.get("password"))
        self.deviceId = kwargs.get("deviceId", "")
        self.profileURL = kwargs.get("profileURL")
        self.landlordAddress = LandlordAddress(**kwargs.get("landlordAddress", {}))

    def initialize_profile(self, firebase, bucketPath):
        blob = firebase.create_blob_no_cache(bucketPath)
        blob.upload_from_string(b"", content_type="image/jpg")
        self.profileURL = blob.public_url

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email ,
            "phoneNumber": self.phoneNumber if self.phoneNumber else "",
            "state": self.state,
            "deviceId": self.deviceId,
            "profileURL": self.profileURL,
            "landlordAddress": self.landlordAddress.to_json() if self.landlordAddress else {},
        }

    def to_dict(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
            "deviceId": self.deviceId,
            "profileURL": self.profileURL
        }
    

class LandlordAddress(Base):
    __tablename__ = "landlord_address"

    id = Column(Integer(), primary_key=True)
    landlord_id = Column(Integer(), ForeignKey("landlord.id"))
    streetNumber = Column(String(10), nullable=False)
    streetName = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False )
    province = Column(String(100), nullable=False)
    postalCode = Column(String(10), nullable=False)
    unitNumber = Column(String(10), nullable=True)
    poBox = Column(String(10), nullable=True)

    def __init__(self, **kwargs):
        self.streetNumber = kwargs.get("streetNumber")
        self.streetName = kwargs.get("streetName")
        self.city = kwargs.get("city")
        self.province = kwargs.get("province")
        self.postalCode = kwargs.get("postalCode")
        self.unitNumber = kwargs.get("unitNumber")
        self.poBox = kwargs.get("poBox")

    def to_dict(self):
        return {
            "landlord_id": self.landlord_id,
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitNumber": self.unitNumber,
            "poBox": self.poBox
        }


    def to_json(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitNumber": self.unitNumber,
            "poBox": self.poBox
        }