from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    language = Column(String)
    # accepted_token = Column(String)
    last_update = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, tg_id, language=''):     # , accepted_token=''
        super().__init__()
        self.tg_id = tg_id
        self.language = language
        # self.accepted_token = accepted_token

    def __repr__(self):
        return f'id: {self.id}, tg_id: {self.tg_id}, language: {self.language}, lastUpdate: {self.last_update}'
