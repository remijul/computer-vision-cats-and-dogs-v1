"""
Script pour s'assurer que la table monitoring_metrics existe dans la base de données
et pour vérifier que le monitoring des inférences fonctionne correctement.
"""
import sqlite3
import sys
import os
from datetime import datetime
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

def get_db_connection():
    """Connexion à la base de données"""
    db_path = os.path.join(ROOT_DIR, 'feedbacks.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Pour avoir des résultats sous forme de dictionnaires
    return conn

def ensure_monitoring_table():
    """S'assurer que la table monitoring_metrics existe"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vérifier si la table existe déjà
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='monitoring_metrics'")
    if cursor.fetchone() is None:
        print("Création de la table monitoring_metrics...")
        # Créer la table si elle n'existe pas
        cursor.execute('''
        CREATE TABLE monitoring_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inference_time_ms FLOAT NOT NULL,
            success BOOLEAN NOT NULL,
            prediction TEXT,
            confidence FLOAT,
            file_size_bytes INTEGER,
            user_agent TEXT,
            error TEXT,
            timestamp DATETIME NOT NULL
        )
        ''')
        
        # Créer les index pour optimiser les requêtes
        cursor.execute('CREATE INDEX idx_metrics_timestamp ON monitoring_metrics(timestamp)')
        cursor.execute('CREATE INDEX idx_metrics_success ON monitoring_metrics(success)')
        
        print("Table monitoring_metrics créée avec succès!")
    else:
        print("La table monitoring_metrics existe déjà.")
    
    conn.commit()
    conn.close()

def check_monitoring_metrics():
    """Vérifier le contenu de la table monitoring_metrics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) AS count FROM monitoring_metrics")
    count = cursor.fetchone()['count']
    print(f"Nombre d'entrées dans monitoring_metrics: {count}")
    
    if count > 0:
        print("\nDernières entrées:")
        cursor.execute("""
        SELECT id, inference_time_ms, success, prediction, confidence, timestamp 
        FROM monitoring_metrics 
        ORDER BY id DESC 
        LIMIT 5
        """)
        
        for row in cursor.fetchall():
            print(f"ID: {row['id']} | Date: {row['timestamp']} | Temps: {row['inference_time_ms']}ms | " +
                  f"Succès: {row['success']} | Prédiction: {row['prediction']} | Confiance: {row['confidence']}")
    
    conn.close()

def add_test_entry():
    """Ajouter une entrée de test dans la table monitoring_metrics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    cursor.execute('''
    INSERT INTO monitoring_metrics 
    (inference_time_ms, success, prediction, confidence, file_size_bytes, user_agent, error, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (123.45, True, "test_prediction", 0.95, 1024, "test_agent", None, timestamp))
    
    print(f"Entrée de test ajoutée avec ID: {cursor.lastrowid}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Vérification de la table monitoring_metrics...")
    ensure_monitoring_table()
    print("\nVérification des métriques actuelles...")
    check_monitoring_metrics()
    
    # Ajouter une entrée de test si demandé
    if len(sys.argv) > 1 and sys.argv[1] == "--add-test":
        print("\nAjout d'une entrée de test...")
        add_test_entry()
        print("\nNouvelles métriques après ajout du test:")
        check_monitoring_metrics()
    
    print("\nTerminé!")