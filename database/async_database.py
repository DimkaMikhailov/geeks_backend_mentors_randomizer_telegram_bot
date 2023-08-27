import asyncio

from config import dbase

from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base as Base
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        self.engine = create_async_engine(dbase)
        self.session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        asyncio.run(self._init_models())

    async def _init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base().metadata.drop_all)
            await conn.run_sync(Base().metadata.create_all)

    async def add_mentor(self, telegram_id, username, month):
        async with self.session as session:
            new_user = Mentor(telegram_id=telegram_id,
                              username=username,
                              month=month)
            session.add(new_user)
            await session.commit()

    async def get_mentor_by_telegram_id(self, telegram_id):
        async with self.session as session:
            query = select(Mentor).where(Mentor.telegram_id == telegram_id)
            result = await session.execute(query)
            mentor = result.scalar()
            return mentor


class Mentor(Base()):
    __tablename__ = 'mentors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    month = Column(String)

    def __repr__(self):
        return f"<Mentor(telegram_id={self.telegram_id}, username='{self.username}', month='{self.month}')>"
