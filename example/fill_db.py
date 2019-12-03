import os
from random import randrange
from datetime import date, timedelta
from django.contrib.auth.hashers import make_password
from django_custom_user_app.models import User, Country, Session, Base, engine


def random_date(start, end):
    """
    This function returns a random datetime between two datetime objects.
    """
    delta = end - start
    random_day = randrange(delta.days)
    return start + timedelta(days=random_day)


# Clearing all tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Filling the tables with test data
d1 = date(1980, 1, 1)
d2 = date(1999, 1, 1)

test_users = (
    ('Anton', 'Lapshin', None, 'iambacon@ya.ru', random_date(d1, d2), 'testpassword1'),
    ('Russell', 'Slater', 'B.', 'RussellBSlater@rhyta.com', random_date(d1, d2), 'testpassword2'),
    ('Robert', 'Willett', 'S.', 'RobertSWillett@rhyta.com', random_date(d1, d2), 'testpassword3'),
    ('Claude', 'Davis', 'D.', 'ClaudeDDavis@teleworm.us', random_date(d1, d2), 'testpassword4'),
    ('Francis', 'Gallo', 'M.', 'FrancisMGallo@rhyta.com', random_date(d1, d2), 'testpassword5'),
    ('Everett', 'Carroll', 'E.', 'EverettECarroll@jourrapide.com', random_date(d1, d2), 'testpassword6'),
)

test_country_objects = [
    Country(name='Russia')
]

test_user_objects = [
    User(
        first_name=user[0],
        last_name=user[1],
        middle_name=user[2],
        email=user[3],
        birth_date=user[4],
        password=make_password(user[5]),
        country_id=1
    ) for user in test_users
]

Session().add_all(test_country_objects)
Session().commit()
Session().add_all(test_user_objects)
Session().commit()
