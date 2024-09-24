from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://postgres:1234@localhost/blockbuster')
# use session_factory() to get a new Session
_session_factory = sessionmaker(bind=engine)


Base = declarative_base()


def session_factory():
   Base.metadata.create_all(engine)
   return _session_factory()