import sqlite3
from datetime import date
from django.conf import settings
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

__all__ = ['Session', 'User', 'Country', 'Token']

# DB initialization from django settings
DB_PROTOCOLS = {
    'django.db.backends.mysql': 'mysql',
    'django.db.backends.postgresql_psycopg2': 'postgres',
}

try:
    db_django_engine = settings.DATABASES['default']['ENGINE']
except (KeyError, AttributeError):
    raise ValueError('Unable to determine current database engine')

# Set db uri from django settings file
if db_django_engine == 'django.db.backends.sqlite3':
    try:
        db_uri = 'sqlite:///{}'.format(settings.DATABASES['default']['NAME'])
    except (KeyError, AttributeError):
        raise ValueError('Unable to determine current database')
elif db_django_engine in DB_PROTOCOLS:
    # Get main db variables from Django settings
    try:
        username = settings.DATABASES['default']['USER']
        db = settings.DATABASES['default']['NAME']
        host = settings.DATABASES['default']['HOST']
    except (KeyError, AttributeError):
        raise ValueError('Unable to get main database variables')

    # Get password and port variables from Django settings
    try:
        password = settings.DATABASES['default']['PASSWORD']
    except (KeyError, AttributeError):
        password = None
    try:
        port = settings.DATABASES['default']['PORT']
    except (KeyError, AttributeError):
        port = None

    # Create db uri
    db_uri = '{}://{}'.format(DB_PROTOCOLS[db_django_engine], username)
    if password is not None and len(password):
        db_uri += ':{}'.format(password)
    db_uri += '@{}'.format(host)
    if port is not None and len(port):
        db_uri += ':{}'.format(port)
    db_uri += '/{}'.format(db)
else:
    raise AttributeError('Unsupported database type: "{}"'.format(db_django_engine))

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
        if isinstance(attrs_dict[attr], date):
            attrs_dict[attr] = str(attrs_dict[attr])
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
    password = Column(String(100), nullable=False)
    country_id = Column(ForeignKey('country.id'))
    tokens = relationship("Token", back_populates="user")

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

    def as_dict(self):
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'birth_date', 'email', 'country_id']
        return class_attrs_to_dict(self, fields)


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(50), nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="tokens")
    expire = Column(Date)
