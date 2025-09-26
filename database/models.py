from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pathlib import Path
import sys
import os

# Ajouter le répertoire racine au path pour accéder à la config
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import DATABASE_CONFIG

# Configuration de la base de données
DATABASE_URL = DATABASE_CONFIG["url"]

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class PredictionFeedback(Base):
    """Modèle pour les feedbacks des prédictions"""
    __tablename__ = "predictions_feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feedback_value = Column(Boolean, nullable=True)  # True=Oui/positif, False=Non/négatif, None=pas de feedback
    date = Column(DateTime, default=datetime.utcnow)
    prediction_result = Column(String, nullable=False)  # 'chat' ou 'chien'
    user_input = Column(Text, nullable=True)  # Input utilisateur (nom de fichier, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PredictionFeedback(id={self.id}, feedback={self.feedback_value}, prediction={self.prediction_result})>"

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction pour créer les tables
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables de base de données créées")

# Fonction pour initialiser la base de données
def init_database():
    create_tables()

if __name__ == "__main__":
    # Créer les tables si le fichier est exécuté directement
    init_database()
    print("Base de données initialisée avec SQLAlchemy")