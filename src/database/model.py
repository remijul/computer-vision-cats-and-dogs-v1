from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Feedback(SQLModel, table=True):
    id: int = Field(primary_key=True)
    feed_back_value: int
    prob_cat: float
    prob_dog: float
    last_modified: datetime

class Monitoring(SQLModel, table=True):
    # Permet à SQLModel de gérer l’auto-incrément :
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    inference_time: float
    succes: bool