from sqlmodel import Field, SQLModel
from datetime import datetime

class Feedback(SQLModel, table=True):
    id: int = Field(primary_key=True)
    feed_back_value: int
    prob_cat: float
    prob_dog: float
    last_modified: datetime

class Monitoring(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime
    inference_time: float
    succes: bool