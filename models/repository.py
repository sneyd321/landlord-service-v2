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

    async def login(self, landlord, password, deviceId):
        monad = await RepositoryMaybeMonad(landlord) \
            .bind_data(self.db.get_landlord_by_email)
        if monad.get_param_at(0) is None:
            return RepositoryMaybeMonad(error_status={"status": 404, "reason": "Invalid email or password"})
        
        if not landlord.verify_password(password, monad.get_param_at(0).password):
            return RepositoryMaybeMonad(error_status={"status": 401, "reason": "Invalid email or password"})
        
        await RepositoryMaybeMonad(landlord) \
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
    

 