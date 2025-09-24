import os
import psycopg2
from psycopg2.extensions import connection as Connection
from config.settings import DB_SETTINGS
import logging

def create_tables_if_not_exist(conn: Connection):
    """Crée les tables 'logs' et 'feedbacks' si elles n'existent pas."""
    with conn.cursor() as cursor:
        # Création de la table logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
                inference_time_ms REAL NOT NULL,
                success BOOLEAN NOT NULL
            );
        ''')
        logging.info("Table 'logs' vérifiée/créée.")

        # Création de la table feedbacks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id SERIAL PRIMARY KEY,
                feedback BOOLEAN NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
                predict_result TEXT NOT NULL,
                input_image BYTEA NOT NULL,
                log_id INTEGER NOT NULL,
                FOREIGN KEY (log_id) REFERENCES logs(id)
            );
        ''')
        logging.info("Table 'feedbacks' vérifiée/créée.")
    conn.commit()

def get_db_connection() -> Connection:
    """
    Établit une connexion à la base de données PostgreSQL.

    Args:
        None

    Returns:
        Connection: La connexion à la base de données.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_SETTINGS["name"],
            user=DB_SETTINGS["user"],
            password=DB_SETTINGS["password"],
            host=DB_SETTINGS["host"],
            port=DB_SETTINGS["port"]
        )
        logging.info(f"Connexion à la base de données PostgreSQL sur {DB_SETTINGS['host']}:{DB_SETTINGS['port']} réussie.")
        
        # Au premier démarrage, on s'assure que les tables existent
        create_tables_if_not_exist(conn)
        
        return conn
    except psycopg2.OperationalError as e:
        logging.error(f"Erreur de connexion à la base de données : {e}")
        # Cette exception sera attrapée par FastAPI ou le code appelant
        raise e
