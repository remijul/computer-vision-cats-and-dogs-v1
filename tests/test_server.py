import uvicorn
from src.api.main import app
import sys
import os
from pathlib import Path

# Définir PYTHONPATH explicitement
ROOT_DIR = Path(__file__).parent
os.environ['PYTHONPATH'] = str(ROOT_DIR)
sys.path.insert(0, str(ROOT_DIR))

try:
    print("Starting server...")
    uvicorn.run(app, host='localhost', port=8000)
except KeyboardInterrupt:
    print("Server stopped by user")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()