import sqlite3
from pathlib import Path
import sys
import os

# Ajouter le répertoire racine au path pour accéder à la config
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import DATABASE_CONFIG

# Configuration de la base de données
DATABASE_PATH = Path(DATABASE_CONFIG["path"])

def get_db_connection():
    """Retourne une connexion à la base de données SQLite"""
    return sqlite3.connect(str(DATABASE_PATH))

def init_database():
    """Initialise la base de données avec la table predictions_feedback"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Créer la table si elle n'existe pas (utiliser le schéma de schema.sql)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feedback_value BOOLEAN,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        prediction_result TEXT,
        user_input TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Créer les index pour optimiser les requêtes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_feedback_date ON predictions_feedback(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_feedback_value ON predictions_feedback(feedback_value)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prediction_result ON predictions_feedback(prediction_result)')

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée avec la table predictions_feedback")

def save_feedback(feedback_value, prediction_result, user_input):
    """Sauvegarde un feedback dans la base de données"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Convertir la valeur du feedback en boolean
    # 'oui' -> True (1), 'non' -> False (0)
    boolean_value = 1 if feedback_value == 'oui' else 0

    cursor.execute('''
    INSERT INTO predictions_feedback (feedback_value, prediction_result, user_input)
    VALUES (?, ?, ?)
    ''', (boolean_value, prediction_result, user_input))

    conn.commit()
    feedback_id = cursor.lastrowid
    conn.close()

    return feedback_id

def get_all_feedbacks():
    """Récupère tous les feedbacks"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM predictions_feedback ORDER BY created_at DESC')
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_feedback_stats():
    """Retourne des statistiques sur les feedbacks"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Compter le nombre total de feedbacks
    cursor.execute('SELECT COUNT(*) FROM predictions_feedback')
    total = cursor.fetchone()[0]

    # Compter les feedbacks positifs (feedback_value = 1)
    cursor.execute('SELECT COUNT(*) FROM predictions_feedback WHERE feedback_value = 1')
    positive = cursor.fetchone()[0]

    # Compter les feedbacks négatifs (feedback_value = 0)
    cursor.execute('SELECT COUNT(*) FROM predictions_feedback WHERE feedback_value = 0')
    negative = cursor.fetchone()[0]

    conn.close()

    return {
        'total_feedbacks': total,
        'positive_feedbacks': positive,
        'negative_feedbacks': negative,
        'accuracy_rate': round((positive / total * 100), 2) if total > 0 else 0
    }

# Initialiser la base de données au premier import
if __name__ != "__main__":
    init_database()