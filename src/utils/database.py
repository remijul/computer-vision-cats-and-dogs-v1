import os
import sqlite3
from sqlite3 import Connection, Cursor

db_path = "data/database.db"

def get_db_connection() -> Connection:
    """
    Créer une base sqlite si elle n'existe pas et retourner une connexion.

    Args:
        db_path (str): Le chemin vers la base de données.

    Returns:
        Connection: La connexion à la base de données.
    """
    if os.path.exists(db_path) == False:
        open(db_path, 'w').close()
    # si elles n'existent pas, créer les tables feedbacks et logs
    if os.path.exists(db_path) and os.path.getsize(db_path) == 0:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                inference_time_ms REAL NOT NULL,
                success BOOLEAN NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feedback TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                predict_result TEXT NOT NULL,
                input_image BLOB NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        print(
            f"Database created at {db_path} (if it doesn't exist).",
        )
    conn = sqlite3.connect(db_path)
    return conn

def close_db_connection(conn: Connection) -> None:
    """
    Fermer la connexion à la base de données.

    Args:
        conn (Connection): La connexion à la base de données.
    """
    conn.close()
