from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, unique=True)
    claimable_token = Column(String)
    accepted_token = Column(String)
    last_update = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, address, claimable_token='', accepted_token=''):
        super().__init__()
        self.address = address
        self.claimable_token = claimable_token
        self.accepted_token = accepted_token

    def __repr__(self):
        return f'id: {self.id}, address: {self.address}, claimable_token: {self.claimable_token}, accepted_token: {self.accepted_token},lastUpdate: {self.last_update}'
