import sqlite3
import os
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent

def add_monitoring_table():
    # Connexion à la base de données existante
    db_path = os.path.join(ROOT_DIR, 'feedbacks.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Création de la table monitoring_metrics
    cursor.executescript('''
    -- Table des métriques de monitoring
    CREATE TABLE IF NOT EXISTS monitoring_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Date et heure de l'inférence
        inference_time_ms FLOAT NOT NULL,             -- Temps d'inférence en millisecondes
        success BOOLEAN NOT NULL,                     -- Si l'inférence a réussi ou échoué
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- Date de création de l'enregistrement
    );

    -- Index pour optimiser les requêtes
    CREATE INDEX IF NOT EXISTS idx_monitoring_timestamp ON monitoring_metrics(timestamp);
    CREATE INDEX IF NOT EXISTS idx_monitoring_success ON monitoring_metrics(success);

    -- Vue pour les statistiques d'inférence
    CREATE VIEW IF NOT EXISTS monitoring_stats AS
    SELECT 
        date(timestamp) as day,
        COUNT(*) as total_inferences,
        AVG(inference_time_ms) as avg_inference_time,
        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate
    FROM monitoring_metrics
    GROUP BY date(timestamp);
    ''')
    
    # Insérer quelques données de test
    cursor.execute('''
    INSERT INTO monitoring_metrics (inference_time_ms, success)
    VALUES 
        (150.5, 1),
        (200.3, 1),
        (180.7, 0)
    ''')
    
    # Valider les changements
    conn.commit()
    
    # Vérifier que la table a été créée et contient les données
    print("\nTable monitoring_metrics créée avec succès!")
    
    print("\nDonnées de test dans monitoring_metrics:")
    cursor.execute('SELECT * FROM monitoring_metrics')
    for row in cursor.fetchall():
        print(row)
    
    print("\nStatistiques de monitoring:")
    cursor.execute('SELECT * FROM monitoring_stats')
    for row in cursor.fetchall():
        print(row)
    
    conn.close()

if __name__ == '__main__':
    add_monitoring_table()