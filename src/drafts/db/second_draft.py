from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey, Table, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func


# Создаем движок базы данных для PostgreSQL
USER = "USER"
PASSWORD = "PASSWORD"
BASE_NAME = "MAIN"

DRIVER = 'postgresql+psycopg2'
HOST = 'localhost'
PORT = '5432'

DB_URL = f'{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{BASE_NAME}'


# Создаем движок базы данных для PostgreSQL
# Замените 'postgresql://username:password@localhost/database' на фактический URL-адрес вашей базы данных PostgreSQL
engine = create_engine(DB_URL, echo=True)
Base = declarative_base()


# Определяем модели и связи таблиц
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String)

    creator_id = Column(Integer, ForeignKey('users.tg_id'))
    creator = relationship('User', back_populates='events_created')
    attendees = relationship('User', secondary='user_event_association', overlaps="events_attended")

    def __init__(self, title="", creator=""):
        self.title = title
        self.creator = creator

    def __repr__(self):
        return f'tg_id: {self.tg_id}'

        # return f"Event(title='{self.title}')"


class User(Base):
    __tablename__ = 'users'
    # id = Column(Integer, primary_key=True)

    tg_id = Column(Integer, primary_key=True)

    language = Column(String)
    name = Column(String)
    info = Column(String)
    city = Column(String)
    sex = Column(String)
    age = Column(String)
    photo = Column(String)

    statuses_edit_user = Column(JSON)
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
            statuses_edit_user="",
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
        self.statuses_edit_user = statuses_edit_user

    def __repr__(self):
        return f'tg_id: {self.tg_id}, language: {self.language}, ' \
               f'name: {self.name}, info: {self.info}, ' \
               f'city: {self.city}, sex: {self.sex}, ' \
               f'age: {self.age}, photo: {self.photo}, ' \
               f'statuses_edit_user: {self.statuses_edit_user}, ' \
               f'lastUpdate: {self.last_update}'

        # return f"User(name='{self.name}')"


user_event_association = Table('user_event_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.tg_id')),
    Column('event_id', Integer, ForeignKey('events.id'))
)

# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Пример использования:
user1 = User(tg_id=31456, name='John Smith')
event1 = Event(title='Event 1', creator=user1)
event2 = Event(title='Event 2', creator=user1)
user2 = User(tg_id=31455, name='User 2')
user3 = User(tg_id=31457, name='User 3')
event1.attendees.append(user2)
event1.attendees.append(user3)
session.add_all([user1, event1, event2, user2, user3])
session.commit()

# Запросы для получения связанных данных
user = session.query(User).filter_by(name='John Smith').first()
print(f"User: {user.name}")
print("Events Created:")
for event in user.events_created:
    print(f"Event: {event.title}")

print("\nEvents Attended:")
for event in user.events_attended:
    print(f"Event: {event.title}")

print()
event = session.query(Event).filter_by(id='1').first()
print(event.title)

print()

event = session.query(Event).filter_by(title='Event 1').first()
attendees = event.attendees

print("Attendees:")
for attendee in attendees:
    print(f"User: {attendee.name}")

print()

user = session.query(User).filter_by(name='User 2').first()
events_attended = user.events_attended

print(f"User: {user.name}")
print("Events Attended:")
for event in events_attended:
    print(f"Event: {event.title}")



# Закрываем сессию
session.close()
