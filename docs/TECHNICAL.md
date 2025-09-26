# Documentation Technique
**Projet** : Classificateur Chats vs Chiens  
**Version** : 1.0  
**Date** : 26 Septembre 2025

## 1. Architecture du Projet

### 1.1 Structure des Dossiers
```
computer-vision-cats-and-dogs/
├── src/
│   ├── api/          # API FastAPI
│   ├── models/       # Modèles ML
│   ├── monitoring/   # Système monitoring
│   └── web/         # Interface utilisateur
├── tests/           # Tests automatisés
├── data/           # Données et modèles
└── config/         # Configuration
```

### 1.2 Technologies Utilisées
- Backend : Python 3.10, FastAPI
- ML : TensorFlow/Keras
- Base de données : SQLite
- Frontend : HTML5, JavaScript, Chart.js
- Tests : pytest
- CI/CD : GitHub Actions

## 2. Composants Principaux

### 2.1 API REST (src/api/)
- Endpoints principaux :
  - `/predict` : Classification d'images
  - `/feedback` : Collecte des retours
  - `/metrics` : Données de monitoring
- Authentification par token
- Rate limiting intégré
- Validation des entrées

### 2.2 Modèle ML (src/models/)
- Architecture : CNN (Convolutional Neural Network)
- Classes : Chat, Chien
- Format d'entrée : Images 224x224 RGB
- Preprocessing intégré
- Inférence optimisée

### 2.3 Monitoring (src/monitoring/)
- Métriques temps réel
- Agrégation des données
- Graphiques interactifs
- Alertes configurables

### 2.4 Interface Web (src/web/)
- Dashboard responsive
- Graphiques Chart.js
- Rafraîchissement automatique
- Filtres temporels

## 3. Base de Données

### 3.1 Schéma
```sql
-- Prédictions
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    image_hash TEXT,
    prediction TEXT,
    confidence REAL,
    inference_time REAL
);

-- Feedbacks
CREATE TABLE feedbacks (
    id INTEGER PRIMARY KEY,
    prediction_id INTEGER,
    feedback_value TEXT,
    timestamp DATETIME
);
```

### 3.2 Maintenance
- Purge automatique > 7 jours
- Indexation optimisée
- Backup quotidien
- Monitoring des performances

## 4. Déploiement

### 4.1 Prérequis
- Python 3.10+
- pip et virtualenv
- Git
- SQLite 3

### 4.2 Installation
```bash
# Cloner le repo
git clone https://github.com/Arno37/computer-vision-cats-and-dogs.git

# Créer environnement virtuel
python -m venv baseenv
source baseenv/bin/activate  # ou baseenv\Scripts\activate sous Windows

# Installer dépendances
pip install -r requirements/prod.txt

# Initialiser la base de données
python -m database.models
```

### 4.3 Configuration
```python
# config/settings.py
DEBUG = False
API_TOKEN = "votre_token"
MODEL_PATH = "data/models/model.h5"
DB_PATH = "data/db.sqlite"
```

## 5. API Reference

### 5.1 Prédiction
```http
POST /api/predict
Content-Type: multipart/form-data
Authorization: Bearer <token>

{
    "image": <file>
}
```

### 5.2 Feedback
```http
POST /api/feedback
Content-Type: application/json
Authorization: Bearer <token>

{
    "prediction_id": "123",
    "feedback": "correct"
}
```

## 6. Monitoring

### 6.1 Métriques Collectées
- Temps d'inférence
- Taux de succès
- Distribution des prédictions
- Précision (via feedback)

### 6.2 Alertes
- Seuils configurables
- Notifications email
- Logs d'erreurs
- Rapports périodiques

## 7. Maintenance

### 7.1 Logs
- Rotation quotidienne
- Niveau INFO en prod
- Format structuré JSON
- Agrégation centralisée

### 7.2 Backup
- Base de données : quotidien
- Modèle ML : versionné
- Métriques : hebdomadaire
- Configuration : Git

## 8. Sécurité

### 8.1 Mesures Implémentées
- HTTPS obligatoire
- Validation des entrées
- Rate limiting
- Tokens sécurisés
- Logs d'accès

### 8.2 Bonnes Pratiques
- Pas de secrets dans le code
- Validation des dépendances
- Updates régulières
- Tests de sécurité