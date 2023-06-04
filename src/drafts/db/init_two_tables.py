# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

# Создаем движок базы данных
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
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='author')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books')
    readers = relationship('Reader', secondary='book_reader_association', overlaps="readers")

class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', secondary='book_reader_association', overlaps="readers")

book_reader_association = Table('book_reader_association', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('reader_id', Integer, ForeignKey('readers.id'))
)

# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Пример использования:
author1 = Author(name='John Smith')
book1 = Book(title='Book 1', author=author1)
book2 = Book(title='Book 2', author=author1)
reader1 = Reader(name='Reader 1')
reader2 = Reader(name='Reader 2')
book1.readers.append(reader1)
book1.readers.append(reader2)
session.add_all([author1, book1, book2, reader1, reader2])
session.commit()

# Запросы для получения связанных данных
author = session.query(Author).filter_by(name='John Smith').first()
print(f"Author: {author.name}")
for book in author.books:
    print(f"Book: {book.title}")
    for reader in book.readers:
        print(f"Reader: {reader.name}")

# Закрываем сессию
session.close()
