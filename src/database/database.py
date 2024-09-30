import os
import uuid


from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from src.GLOBAL import GLOBAL

"""
This module contains the database logic for the application.

It creates a database engine and session using SQLite as the database.
The database stores the user's account information, including the uuid, account name, proxy and user agent.
The cookies are also stored in the database.

The module also contains a class for the Account database model.
"""

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    uuid = Column(String, primary_key=True, default=str(uuid.uuid4()))
    account_name = Column(String, unique=True, nullable=False)
    # allows proxy and user agent to be optional
    proxy = Column(Text, nullable=True)
    user_agent = Column(Text, nullable=True)
    cookies = Column(Text, nullable=False)


engine = create_engine('sqlite:///accounts.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
