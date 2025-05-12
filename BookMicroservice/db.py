from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
import os

DATABASE_URL = "postgresql://postgres:EmasT2024.@localhost/FromMonolithicToMicro"


engine = create_engine(DATABASE_URL, connect_args={})


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
