from config.settings import DB_CONFIG
from sqlalchemy import URL
from sqlmodel import Field, SQLModel, create_engine, Session
from datetime import datetime, timezone

#Chargement en memoire et modification des metadata de l'ORM
from .model import *

def get_utc_timestamp():
    return datetime.now(timezone.utc).replace(tzinfo=None)

# Création URL avec la fonction SQLAlchemy
POSTGRES_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    host=DB_CONFIG["host"],
    database=DB_CONFIG["name"],
)

engine = create_engine(POSTGRES_URL, echo=True)

def create_tables():
    global engine

    SQLModel.metadata.create_all(engine)

def drop_tables():
    global engine
    
    SQLModel.metadata.drop_all(engine)

def insert_feedback(id, value, prob_cat, prob_dog):
    global engine
    
    feedback = Feedback(id=id,feed_back_value=value, prob_cat=prob_cat, prob_dog=prob_dog, last_modified=get_utc_timestamp())

    with Session(engine) as conn:
        conn.add(feedback)
        conn.commit()

def insert_monitoring(id, time, succes):
    global engine

    monitoring = Monitoring(id=id, timestamp=get_utc_timestamp(), inference_time=time, succes=succes)

    with Session(engine) as conn:
        conn.add(monitoring)
        conn.commit()


if __name__ == "__main__":
    #create_tables()
    #insert_feedback(1, 2, 0.7, 0.3)
    #insert_monitoring(1, 2.5, True)
    pass