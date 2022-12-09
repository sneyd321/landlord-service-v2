from models.models import Landlord, LandlordAddress
from models.monad import RepositoryMaybeMonad

class Repository:

    def __init__(self, db):
        self.db = db  

    async def insert(self, landlord, firebase, isTest=False):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(landlord.email).bind_data(self.db.get_landlord_by_email)
            landlordFromDB = monad.get_param_at(0)
            if landlordFromDB is not None:
                return RepositoryMaybeMonad(None, error_status={"status": 409, "reason": f"Account already exists with email: {landlord.email}"})
            
            monad = await RepositoryMaybeMonad(landlord).bind(self.db.insert)
            if monad.has_errors():
                await RepositoryMaybeMonad().bind(self.db.rollback) 
                return monad
            await RepositoryMaybeMonad().bind(self.db.commit)

            if isTest:
                landlord.initialize_profile(firebase, f"Test/Landlord_{landlord.id}.jpg")
            else:
                landlord.initialize_profile(firebase, f"Profiles/Landlord/Landlord_{landlord.id}.jpg")
            monad = await RepositoryMaybeMonad(landlord).bind(self.db.update)
            if monad.has_errors():
                await RepositoryMaybeMonad().bind(self.db.rollback) 
                return monad
            await RepositoryMaybeMonad().bind(self.db.commit)
            
            return monad

    async def login(self, email, password, deviceId):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(email).bind_data(self.db.get_landlord_by_email)
            landlordFromDB = monad.get_param_at(0)
            if landlordFromDB is None:
                return RepositoryMaybeMonad(error_status={"status": 404, "reason": "Invalid email or password"})
            
            if not landlordFromDB.verify_password(password, landlordFromDB.password):
                return RepositoryMaybeMonad(error_status={"status": 401, "reason": "Invalid email or password"})
            
            landlordFromDB.deviceId = deviceId
            monad = await RepositoryMaybeMonad(landlordFromDB).bind(self.db.update)
            if monad.has_errors():
                await RepositoryMaybeMonad().bind(self.db.rollback)
                return monad
            await RepositoryMaybeMonad().bind(self.db.commit)
            return monad
        

    async def get_landlord(self, landlordId):
        async with self.db.get_session():
            landlord = Landlord(password="")
            landlord.id = landlordId
            print(landlord.to_json())
            monad = await RepositoryMaybeMonad(landlord).bind_data(self.db.get)
            if monad.get_param_at(0) is None:
                return RepositoryMaybeMonad(None, error_status={"status": 404, "reason": f"Landlord not found with id: {landlord.id}"})
            return monad

    async def update(self, landlord):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(landlord.email).bind_data(self.db.get_landlord_by_email)
            landlordFromDB = monad.get_param_at(0)
            if landlordFromDB is None:
                return RepositoryMaybeMonad(None, error_status={"status": 404, "reason": f"Landlord not found with id: {landlord.id}"})

            landlord.id = landlordFromDB.id
            monad = await RepositoryMaybeMonad(landlord).bind(self.db.update)
            if monad.has_errors():
                await RepositoryMaybeMonad().bind(self.db.rollback)
                return monad
            await RepositoryMaybeMonad().bind(self.db.commit)
            return monad

    async def delete(self, landlord):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(landlord.email).bind_data(self.db.get_landlord_by_email)
            landlordFromDB = monad.get_param_at(0)
            if landlordFromDB is None:
                return RepositoryMaybeMonad(None, error_status={"status": 404, "reason": f"Landlord not found with id: {landlord.id}"})
            
            landlord.id = landlordFromDB.id
            monad = await RepositoryMaybeMonad(LandlordAddress, LandlordAddress.landlord_id, landlord.id).bind(self.db.delete_by_column_id)
            if monad.has_errors():
                await RepositoryMaybeMonad().bind(self.db.rollback)
                return monad

            monad = await RepositoryMaybeMonad(landlord).bind(self.db.delete)
            if monad.has_errors():
                await RepositoryMaybeMonad().bind(self.db.rollback)
                return monad
            await RepositoryMaybeMonad().bind(self.db.commit)
            return monad
    
 