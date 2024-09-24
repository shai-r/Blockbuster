from config.base import Base, engine

def create_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)