from config.base import Base, engine

def create_tables():
    Base.metadata.create_all(engine)