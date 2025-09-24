import sys
from pathlib import Path
from sqlmodel import create_engine

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from maconfig import DATABASE_URL

print(f"Connecting to database at {DATABASE_URL}")
# Créer l'engine une seule fois
engine = create_engine(DATABASE_URL, echo=True)