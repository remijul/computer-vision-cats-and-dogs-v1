import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

try:
    print("Testing imports...")
    from src.api.routes import router
    print("✅ Routes import successful")
except Exception as e:
    print(f"❌ Routes import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from database import init_database
    print("✅ Database import successful")
    init_database()
    print("✅ Database init successful")
except Exception as e:
    print(f"❌ Database import/init failed: {e}")
    import traceback
    traceback.print_exc()