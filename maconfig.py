import os
from pathlib import Path
from dotenv import load_dotenv


# Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = os.path.join(BASE_DIR, "data")

# Loading environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)


# PostgreSQL configuration
DB_NAME = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD") # Assurez-vous d'utiliser un mot de passe sécurisé
PG_HOST = "localhost"
PG_PORT = "5432"
DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}"


