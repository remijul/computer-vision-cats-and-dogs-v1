# Documentation Technique - Cats vs Dogs Classifier

## Architecture Détaillée

### Vue d'Ensemble du Système
![Architecture système](img/system_architecture.png)

L'application est construite en utilisant une architecture en couches :
- **Frontend** : Interface web responsive
- **API** : FastAPI RESTful
- **ML** : TensorFlow/Keras
- **Storage** : SQLite + CSV

### Flux de Données
![Flux de données](img/data_flow.png)

1. **Soumission d'image**
   - Upload via interface web
   - Validation format et taille
   - Prétraitement pour le modèle

2. **Traitement**
   - Normalisation image
   - Inférence modèle
   - Génération résultats

3. **Stockage**
   - Enregistrement feedback
   - Métriques de performance
   - Logs système

## Composants Techniques

### 1. Frontend
![Frontend](img/frontend_components.png)

- **Technologies** :
  - HTML5/CSS3
  - JavaScript
  - Bootstrap 5
  - Templates Jinja2

- **Fonctionnalités** :
  - Upload d'images
  - Affichage prédictions
  - Interface feedback
  - Dashboard monitoring

### 2. Backend API
![Backend](img/backend_components.png)

- **Technologies** :
  - FastAPI
  - Python 3.10+
  - SQLAlchemy
  - Pydantic

- **Endpoints** :
  ```
  POST /api/predict
  POST /api/feedback
  GET /api/metrics
  GET /api/health
  ```

### 3. Modèle ML
![ML](img/ml_components.png)

- **Architecture** :
  - CNN TensorFlow
  - Transfer Learning
  - Data Augmentation

- **Performances** :
  - Précision : 95%+
  - Temps inférence : <500ms
  - Taille modèle : 85MB

### 4. Base de Données
![Database](img/database_schema.png)

```sql
CREATE TABLE predictions_feedback (
    id INTEGER PRIMARY KEY,
    feedback_value BOOLEAN,
    date DATETIME,
    prediction_result TEXT,
    user_input TEXT
);
```

## Monitoring et Métriques

### Dashboard Temps Réel
![Dashboard](img/monitoring_dashboard.png)

- **Métriques clés** :
  - Taux de succès
  - Temps de réponse
  - Utilisation ressources

### Graphiques Performance
![Performance](img/performance_graphs.png)

- **Visualisations** :
  - Tendances prédictions
  - Distribution erreurs
  - Feedback utilisateur

## Sécurité

### Authentification
![Security](img/security_components.png)

- Token-based auth
- Rate limiting
- Validation entrées

### Protection Données
- Anonymisation
- Logs sécurisés
- Backup régulier

## Maintenance

### Déploiement
![Deployment](img/deployment_flow.png)

1. Tests automatisés
2. Build Docker
3. Déploiement continu

### Monitoring
![Monitoring](img/monitoring_flow.png)

- Alertes automatiques
- Backup journalier
- Rotation logs

## Guide Développeur

### Setup Environnement
```bash
# Création env
python -m venv baseenv

# Installation deps
pip install -r requirements.txt

# Lancement serveur
uvicorn src.api.main:app
```

### Tests
```bash
# Tests unitaires
pytest tests/

# Coverage
pytest --cov=src
```

### Documentation API
![API Docs](img/api_docs.png)

Swagger UI disponible sur `/docs`