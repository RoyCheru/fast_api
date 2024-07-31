from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from .config import settings
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:gracious2024@localhost:5432/fast api"
#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

#we are not using this below ,its just for referencing. Connecting to the database

#while True:
#try:
    #conn = psycopg2.connect(host='localhost', database='fast api', user='postgres', password='gracious2024',
    #cursor_factory=RealDictCursor)
    #cursor = conn.cursor()
    #print("Database connection was succesful")
    #break
#except Exception as error:
    #print("connecting to database failed")
    #print("Error:", error)
    #time.sleep(2)
