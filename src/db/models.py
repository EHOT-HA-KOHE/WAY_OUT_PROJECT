from sqlalchemy import Column, String, DateTime, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    tg_id = Column(Integer, primary_key=True)   # , autoincrement=True

    language = Column(String)
    name = Column(String)
    info = Column(String)
    city = Column(String)
    sex = Column(String)
    age = Column(String)
    photo = Column(String)

    statuses = Column(JSON)

    # accepted_token = Column(String)
    last_update = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(
            self,
            tg_id,
            language="",
            name="",
            info="",
            city="",
            sex="",
            age="",
            photo="",
            statuses="",
    ):     # , accepted_token=''

        super().__init__()
        self.tg_id = tg_id
        self.language = language
        self.name = name
        self.info = info
        self.city = city
        self.sex = sex
        self.age = age
        self.photo = photo
        self.statuses = statuses
        # self.accepted_token = accepted_token

    def __repr__(self):
        return f'tg_id: {self.tg_id}, language: {self.language}, ' \
               f'name: {self.name}, info: {self.info}, ' \
               f'city: {self.city}, sex: {self.sex}, ' \
               f'age: {self.age}, photo: {self.photo}, ' \
               f'statuses: {self.statuses}, ' \
               f'lastUpdate: {self.last_update}'    #  accepted_token=: {self.accepted_token},
