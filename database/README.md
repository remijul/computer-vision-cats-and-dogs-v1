# Base de Données - Feedbacks Utilisateur

## Vue d'ensemble
La base de données SQLite `feedbacks.db` stocke les feedbacks des utilisateurs sur les prédictions du modèle de classification chats/chiens.

## Structure de la table `predictions_feedback`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Identifiant unique auto-incrémenté |
| `feedback_value` | BOOLEAN | Valeur du feedback (1=Oui/positif, 0=Non/négatif, NULL=pas de feedback) |
| `date` | DATETIME | Date et heure du feedback |
| `prediction_result` | TEXT | Résultat de la prédiction ('chat' ou 'chien') |
| `user_input` | TEXT | Input utilisateur (nom du fichier image, etc.) |
| `created_at` | DATETIME | Timestamp automatique de création |

## Utilisation

### Avec SQLAlchemy (recommandé)
```python
from database.models import PredictionFeedback, SessionLocal

# Créer une session
db = SessionLocal()

# Ajouter un feedback
new_feedback = PredictionFeedback(
    feedback_value=True,  # True pour positif, False pour négatif
    prediction_result="chat",
    user_input="image_chat.jpg"
)
db.add(new_feedback)
db.commit()

# Récupérer tous les feedbacks
feedbacks = db.query(PredictionFeedback).all()

db.close()
```

### Avec SQLite directement
```python
import sqlite3

conn = sqlite3.connect('feedbacks.db')
cursor = conn.cursor()

# Insérer un feedback
cursor.execute('''
INSERT INTO predictions_feedback (feedback_value, prediction_result, user_input)
VALUES (?, ?, ?)
''', (True, 'chat', 'image.jpg'))

conn.commit()
conn.close()
```

## Scripts disponibles

- `database/__init__.py` : Fonctions utilitaires pour la base de données
- `database/models.py` : Modèles SQLAlchemy
- `database/schema.sql` : Schéma SQL de la base de données
- `test_database.py` : Script de test des fonctionnalités

## Statistiques

La base de données permet de calculer :
- Nombre total de feedbacks
- Taux de feedbacks positifs/négatifs
- Taux de précision du modèle basé sur les feedbacks utilisateur

## Initialisation

Pour initialiser la base de données :
```python
from database.models import init_database
init_database()
```

Ou exécuter :
```bash
python -c "from database.models import init_database; init_database()"
```