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
    # si elles n'existent pas, créer les tables feedbacks et logs, seulement si les tables n'existent pas
    if os.path.exists(db_path):
        # vérifier les tables existantes
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='logs';
        ''')
        logs_table_exists = cursor.fetchone() is not None

        cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='feedbacks';
        ''')
        feedbacks_table_exists = cursor.fetchone() is not None

        cursor.close()

        if not logs_table_exists:
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
            conn.commit()
            cursor.close()
            print(
                f"Table 'logs' created in database at {db_path} (if it doesn't exist).",
            )
        if not feedbacks_table_exists:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE feedbacks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feedback BOOLEAN NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    predict_result TEXT NOT NULL,
                    input_image BLOB NOT NULL,
                    log_id INTEGER NOT NULL,
                    FOREIGN KEY (log_id) REFERENCES logs(id)
                )
            ''')
            conn.commit()
            cursor.close()
            print(
                f"Table 'feedbacks' created in database at {db_path} (if it doesn't exist).",
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
