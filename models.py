from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func
from flask_login import UserMixin

engine = create_engine('postgresql://admin1:admin1pwd@127.0.0.1:5431/netology_ad_db')
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Advertisement(Base):
    __tablename__ = 'app_ad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    creation_time = Column(DateTime, server_default=func.now())
    author = Column(String)

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)


Base.metadata.create_all()
