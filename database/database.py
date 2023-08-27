from config import dbase

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = create_engine(dbase)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user(self, username, email):
        new_user = Mentor(username=username, email=email)
        self.session.add(new_user)
        self.session.commit()

    def get_user_by_username(self, username):
        mentor = self.session.query(Mentor).filter_by(username=username).first()
        return mentor


class Mentor(Base):
    __tablename__ = 'mentors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    month = Column(String)

    def __repr__(self):
        return f"<Mentor(telegram_id={self.telegram_id}, username='{self.username}', month='{self.month}')>"
