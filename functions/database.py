from sqlalchemy import create_engine, Column, MetaData, inspect, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.testing.schema import Table
from sqlalchemy.types import Text, Date
import sys

base = declarative_base()


class Einrichtung(base):
    __tablename__ = 'Einrichtungen'

    name = Column(Text, primary_key=True)
    street = Column(Text)
    postcode = Column(Text)
    city = Column(Text)
    telefon = Column(Text)
    email = Column(Text)
    web = Column(Text)
    degree = Column(Text)
    parttime_education = Column(Text)
    certificate = Column(Text)
    district_code = Column(Text)
    inserted = Column(Date)
    updated = Column(Date)


def get_engine(db):

    try:
        db_string = f"postgresql://admin:admin@localhost:5432/{db}"
        engine = create_engine(db_string, pool_size=50, echo=False)
        return engine
    except Exception as get_engine_err:
        print('Something happened in get_engine')
        print(sys.exc_info())
        print(get_engine_err)


def get_session(engine):

    try:
        session = sessionmaker(engine, autocommit=True)
        return session
    except Exception as get_session_err:
        print('Something happened in get_session')
        print(sys.exc_info())
        print(get_session_err)


def db_connect(db):

    try:
        engine = get_engine(db)
        session = get_session(engine)
        active_session = session()
        base.metadata.create_all(engine)
        return {'session': active_session, 'engine': engine}
    except Exception as db_connect_err:
        print('Something happened in db_connect')
        print(sys.exc_info())
        print(db_connect_err)


def write_db(inserts, db):

    try:
        to_delete = delete(Einrichtung.__table__)
        response = db_connect(db)
        session = response['session']
        to_insert = insert(Einrichtung.__table__).values(inserts)
        session.execute(to_delete)
        session.execute(to_insert)
        return session
    except Exception as write_db_err:
        print('Something happened in write_db')
        # print(sys.exc_info())
        # print(write_db_err)
    finally:
        session.close()


def read_db(session):
    print('Hello')


def create_table():
    engine = get_engine('pflege_ausbildung')
    if not inspect(engine).has_table('Einrichtungen'):
        metadata = MetaData(engine)
        Table('Einrichtungen', metadata,
              Column('name', Text, primary_key=True, unique=True),
              Column('street', Text),
              Column('postcode', Text),
              Column('city', Text),
              Column('telefon', Text),
              Column('email', Text),
              Column('web', Text),
              Column('degree', Text),
              Column('parttime_education', Text),
              Column('certificate', Text),
              Column('district_code', Text),
              Column('inserted', Date),
              Column('updated', Date))
        base.metadata.create_all(engine)
