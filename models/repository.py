from models.models import Landlord
from models.monad import RepositoryMaybeMonad

class Repository:

    def __init__(self, db):
        self.db = db  

    async def insert(self, landlord):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(landlord) \
                .bind_data(self.db.get_landlord_by_email)
            if monad.get_param_at(0):
                return RepositoryMaybeMonad(None, error_status={"status": 409, "reason": "Failed to insert data into database"})
            await RepositoryMaybeMonad(landlord) \
                .bind(self.db.insert)
            return await RepositoryMaybeMonad() \
                .bind(self.db.commit)

    async def login(self, login, password, deviceId):
        monad = await RepositoryMaybeMonad(login) \
            .bind_data(self.db.get_landlord_by_email)
        landlordFromDB = monad.get_param_at(0)
        if landlordFromDB is None:
            return RepositoryMaybeMonad(error_status={"status": 404, "reason": "Invalid email or password"})
        
        if not login.verify_password(password, landlordFromDB.password):
            return RepositoryMaybeMonad(error_status={"status": 401, "reason": "Invalid email or password"})
        

        landlordFromDB.deviceId = deviceId
        monad = await RepositoryMaybeMonad(landlordFromDB) \
            .bind(self.db.update)
        
        if monad.has_errors():
            return monad
        await RepositoryMaybeMonad() \
            .bind(self.db.commit)
        return monad
        

    async def get_landlord(self, landlord):
        async with self.db.get_session():
            return await RepositoryMaybeMonad(landlord) \
                .bind_data(self.db.get)
    

    async def delete(self, landlord):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(landlord) \
                .bind_data(self.db.get)
            landlordFromDB = monad.get_param_at(0)
            if landlordFromDB is None:
                return RepositoryMaybeMonad(None, error_status={"status": 404, "reason": f"Landlord not found with id: {landlord.id}"})
            monad = await RepositoryMaybeMonad(landlordFromDB) \
                .bind(self.db.delete)
            print(monad.error_status)

            await RepositoryMaybeMonad() \
                .bind(self.db.commit)
            return monad
    
 