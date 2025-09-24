from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date

class Prediction(SQLModel, table=True):
    id_predict: Optional[int] = Field(default=None, primary_key=True)
    date_prediction: datetime= Field(default_factory=datetime.now)
    probabilite_chat: float = Field(ge=0, le=1)
    image_path: str
    inference_time_ms: float

    feedback: Optional["Feedback"] = Relationship(back_populates="prediction")

class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prediction_id: int = Field(foreign_key="prediction.id_predict")
    feedback: bool
    
    prediction: Prediction = Relationship(back_populates="feedback")