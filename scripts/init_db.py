import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from sqlmodel import SQLModel
from src.database.db_engine import engine
from src.database.db_models import Prediction, Feedback # sans cette ligne ne fonctionne pas ????

def init_db():
    print("Création des tables dans la base de données...")
    print(f"init_db : {engine}")
    SQLModel.metadata.create_all(engine)
    print("Tables créées avec SQLModel.")

if __name__ == "__main__":
    
    init_db()
