from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import sessionmaker, relationship, joinedload

from config import db

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, REAL, ForeignKey, UniqueConstraint, update

import json

Base = declarative_base()


class Mentor(Base):
    __tablename__ = 'mentors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    in_chart = Column(Boolean, default=False)
    month = Column(Integer, default=1)
    mentor = Column(Boolean, default=True)

    mentor_rating = relationship('MentorsRating', backref='mentors')

    def __repr__(self):
        mentor = {
            'mentor': self.mentor,
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'month': self.month,
            'in_chart': self.in_chart,
        }
        return json.dumps(mentor)


class MentorsRating(Base):
    __tablename__ = 'mentors_rating'

    id = Column(Integer, primary_key=True, autoincrement=True)
    request = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    failure = Column(Integer, default=0)
    rating = Column(REAL, default=1)
    mentor_telegram_id = Column(Integer, ForeignKey('mentors.telegram_id'))
    UniqueConstraint(mentor_telegram_id)

    def __repr__(self):
        mentor_rating = {
            'request': self.request,
            'wins': self.wins,
            'failure': self.failure,
            'rating': self.rating,
            'mentors_telegram_id': self.mentor_telegram_id
        }
        return json.dumps(mentor_rating)


class Database:
    def __init__(self):
        self.engine = create_async_engine(db)
        session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session = session()

    async def init_models(self):
        async with self.engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
            print(f'[INFO] tables create successfully')

    async def add_user(self,
                       telegram_id: int,
                       username: str,
                       first_name: str,
                       last_name: str,
                       in_chart=None,
                       month=1,
                       mentor=True) -> None:
        async with self.session as session:
            try:
                new_user = Mentor(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    in_chart=in_chart,
                    month=month,
                    mentor=mentor)

                session.add(new_user)
                await session.commit()
                print(f'[INFO] user add successfully')
            except IntegrityError:
                await session.rollback()
                print(f'[INFO] user already exists')

    async def add_mentor_to_mentors_rating(self,
                                           mentor_telegram_id: int,
                                           request=None,
                                           wins=None,
                                           failure=None,
                                           rating=None) -> None:
        async with self.session as session:
            try:
                new_user = MentorsRating(
                    request=request,
                    wins=wins,
                    failure=failure,
                    rating=rating,
                    mentor_telegram_id=mentor_telegram_id)

                session.add(new_user)
                await session.commit()
                print(f'[INFO] user add to mentors rating successfully')
            except IntegrityError as e:
                await session.rollback()
                print(f'[INFO] user in mentors rating already exists', e)

    async def get_user(self, by_username=None, by_first_name=None, by_telegram_id=None):
        async with self.session as session:
            try:
                if by_telegram_id:
                    query = select(Mentor).where(Mentor.telegram_id == by_telegram_id)
                elif by_username:
                    query = select(Mentor).where(Mentor.username == by_username)
                elif by_first_name:
                    query = select(Mentor).where(Mentor.first_name == by_first_name)
            except AttributeError:
                print('[INFO] get_user: not in table')

            result = await session.execute(query)
            mentor = result.scalar()
            return mentor

    async def update_user(self, telegram_id, **kwargs):
        async with self.session as session:
            try:
                query = update(Mentor).where(Mentor.telegram_id == telegram_id).values(kwargs)
                await session.execute(query)
                await session.commit()
                print(f'[INFO] update Mentor: {kwargs}')

            except NoResultFound as e:
                await session.rollback()
                print('[INFO] update Mentor -> False', e)

    async def update_mentor_rating(self, telegram_id: int) -> None:
        async with self.session as session:
            try:
                query = select(MentorsRating.request)
                result = await session.execute(query)
                count = int(result.scalar())
                try:
                    query = update(MentorsRating).values(request=count + 1)
                    await session.execute(query)
                    await session.commit()
                    print(f'[INFO] request: {count + 1}')
                except IntegrityError as e:
                    print('[INFO] update mentors rating -> False', e)

                try:
                    query = update(MentorsRating) \
                        .where(MentorsRating.mentor_telegram_id == telegram_id) \
                        .values(wins=MentorsRating.wins + 1)
                    await session.execute(query)
                    await session.commit()
                    print(f'[INFO] wins: + 1')
                except IntegrityError as e:
                    print('[INFO] update mentors wins -> False', e)

            except NoResultFound as e:
                print('[INFO] select request -> False', e)

    async def select_all_users(self) -> list:
        async with self.session as session:
            try:
                query = select(Mentor)
                result = await session.execute(query)
                mentors_list = result.all()
                print('[INFO] select all users -> Done')
                mentors = [i[0] for i in mentors_list]
                return mentors
            except NoResultFound as e:
                print('[INFO] select all users ->', e)
                return []

    async def select_mentors(self, by_month: int) -> list:
        async with self.session as session:
            try:
                query = select(Mentor).where(Mentor.month > by_month)
                result = await session.execute(query)
                mentors = [i[0] for i in result.all()]
                print(f'[INFO] select mentors {by_month=}')
                return mentors
            except Exception as e:
                print(f'[INFO] select mentors by {by_month=} -> False', e)
                return []

    async def select_all_mentors_with_rating(self) -> list:
        async with self.session as session:
            try:
                query = select(Mentor).options(joinedload(Mentor.mentor_rating))
                result = await session.execute(query)
                mentors_rating_list = []
                if result.unique():
                    for mentor in result.scalars():
                        mentors_rating_list.append(
                            {"mentor": mentor,
                             "rating": mentor.mentor_rating[0]})
                    print('[INFO] select all mentors with rating -> Done')
                    return mentors_rating_list

            except Exception as e:
                print(f'[INFO] select mentors with rating -> False', e)
                return []

    async def select_one_mentor_with_rating(self, telegram_id: int) -> dict:
        async with self.session as session:
            try:
                query = select(MentorsRating).where(MentorsRating.mentor_telegram_id == telegram_id)
                result = await session.execute(query)
                if mentor_rating := result.scalar():
                    print('[INFO] select one mentor rating -> Done')
                    return mentor_rating
            except Exception as e:
                print(f'[INFO] select one mentor rating -> False', e)
                return {}


