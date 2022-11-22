from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from models.models import Landlord
from sqlalchemy import func

class DB:

    def __init__(self, user, password, host, database):
        self.engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{database}", pool_pre_ping=True)
        
        Session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session = Session()
        try:
            _ = self.session.connection()
        except PendingRollbackError:
            self.session.rollback()
        
    def get_session(self):
        return self.session
        
    async def get(self, data):
        result = await self.session.execute(select(Landlord).where(Landlord.id == data.id))
        return result.scalars().first()

    async def get_landlord_by_email(self, data):
        result = await self.session.execute(select(Landlord).where(Landlord.email == data.email))
        return result.scalars().first()

    async def insert(self, data):
        self.session.add(data)

    async def delete(self, data):
        await self.session.execute(delete(Landlord).where(Landlord.id == data.id))
            
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
    
    async def update(self, data):
        await self.session.execute(update(Landlord).where(Landlord.id == data.id).values(data.to_dict()))
       