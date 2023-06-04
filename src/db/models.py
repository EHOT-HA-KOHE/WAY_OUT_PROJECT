from sqlalchemy import Column, String, DateTime, Integer, JSON, ForeignKey, Table, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)

    language = Column(String)
    title = Column(String)
    description = Column(String)
    city = Column(String)
    max_amount_of_people = Column(String)
    date = Column(String)
    photo = Column(String)
    location = Column(String)

    temp_info = Column(JSON)
    creator_id = Column(Integer, ForeignKey('users.tg_id'))

    creator = relationship('User', back_populates='events_created')
    attendees = relationship('User', secondary='user_event_association', overlaps="events_attended")
    categories = relationship('Category', secondary='event_category_association', back_populates='events')

    def __init__(
            self, title="", creator="", language="", description="", city="", max_amount_of_people="",
            date="", photo="", location="",  temp_info="", creator_id="",
    ):
        self.language = language
        self.title = title
        self.creator = creator
        self.description = description
        self.city = city
        self.max_amount_of_people = max_amount_of_people
        self.date = date
        self.photo = photo
        self.location = location
        self.temp_info = temp_info
        self.creator_id = creator_id

    def __repr__(self):
        return f'language: {self.language}, title: {self.title}, creator: {self.creator}, ' \
               f'description: {self.description}, city: {self.city}, max_amount_of_people: {self.max_amount_of_people}, ' \
               f'date: {self.date}, photo: {self.photo}, location: {self.location}, ' \
               f'temp_info: {self.temp_info}, creator_id: {self.creator_id}' \



class User(Base):
    __tablename__ = 'users'
    tg_id = Column(BigInteger, primary_key=True)

    language = Column(String)
    name = Column(String)
    info = Column(String)
    city = Column(String)
    sex = Column(String)
    age = Column(String)
    photo = Column(String)
    status = Column(String)

    statuses_edit_user = Column(JSON)
    statuses_edit_event = Column(JSON)

    last_update = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    events_created = relationship('Event', back_populates='creator')
    events_attended = relationship('Event', secondary='user_event_association', overlaps="events_attended")

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
            status="",
            statuses_edit_user="",
            statuses_edit_event="",
    ):
        super().__init__()
        self.tg_id = tg_id
        self.language = language
        self.name = name
        self.info = info
        self.city = city
        self.sex = sex
        self.age = age
        self.photo = photo
        self.status = status
        self.statuses_edit_user = statuses_edit_user
        self.statuses_edit_event = statuses_edit_event

    def __repr__(self):
        return f'tg_id: {self.tg_id}, language: {self.language}, ' \
               f'name: {self.name}, info: {self.info}, ' \
               f'city: {self.city}, sex: {self.sex}, ' \
               f'age: {self.age}, photo: {self.photo}, status: {self.status}, ' \
               f'statuses_edit_user: {self.statuses_edit_user}, statuses_edit_event: {self.statuses_edit_event}, ' \
               f'lastUpdate: {self.last_update}'


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    events = relationship('Event', secondary='event_category_association', back_populates='categories')

    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return f'name: {self.name}'


user_event_association = Table(
    'user_event_association',
    Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.tg_id')),
    Column('event_id', Integer, ForeignKey('events.id'))
)

event_category_association = Table(
    'event_category_association',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)
