import sqlite3
from django.conf import settings
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['Session', 'User', 'Country']

# DB initialization from django settings
# TODO: Add MySQL and PostgreSQL support
try:
    db_uri = 'sqlite:///{}'.format(settings.DATABASES['default']['NAME'])
except (KeyError, AttributeError):
    raise ValueError('Unable to determine current database')
engine = create_engine(db_uri)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# Enabling foreign keys constraints check for sqlite db
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    if isinstance(dbapi_connection, sqlite3.Connection):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")


def class_attrs_to_dict(in_object, attrs):
    attrs_dict = {}
    for attr in attrs:
        attrs_dict[attr] = getattr(in_object, attr)
    return attrs_dict


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f'{self.name}'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    middle_name = Column(String(50))
    birth_date = Column(Date)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    country_id = Column(ForeignKey('country.id'))

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

    def as_dict(self):
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'birth_date', 'email']
        return class_attrs_to_dict(self, fields)
