# Tests Automatisés

## Structure des Tests

Les tests sont organisés par catégorie fonctionnelle :

### 1. Tests API (`/api`)
- `test_api.py` : Tests des endpoints principaux
- `test_api_simple.py` : Tests API basiques
- `test_api_feedback.py` : Tests des endpoints de feedback
- `test_feedback.py` : Tests de la logique de feedback

### 2. Tests Base de Données (`/database`)
- `test_database.py` : Tests des opérations CRUD
- Fixtures de base de données de test

### 3. Tests Monitoring (`/monitoring`)
- `test_monitoring.py` : Tests du système de monitoring
- `test_metrics.py` : Tests des calculs de métriques

### 4. Tests Modèle (`/model`)
- `test_models.py` : Tests du modèle ML
- `test_predictor.py` : Tests du prédicteur
- `test_predict_simple.py` : Tests simples de prédiction

### 5. Tests Performance (`/performance`)
- `test_performance.py` : Tests de charge et performance

### 6. Tests Infrastructure (`/infrastructure`)
- `test_server.py` : Tests du serveur
- `test_health.py` : Tests de santé

### 7. Tests Utilitaires (`/utils`)
- `test_imports.py` : Tests des imports
- `test_json.py` : Tests de sérialisation
- `test_simple.py` : Tests utilitaires divers

## Exécution des Tests

### Tous les tests
```bash
pytest tests/ -v
```

### Par catégorie
```bash
pytest tests/api/ -v         # Tests API
pytest tests/database/ -v    # Tests Base de données
pytest tests/monitoring/ -v  # Tests Monitoring
pytest tests/model/ -v      # Tests Modèle
pytest tests/performance/ -v # Tests Performance
```

### Avec couverture
```bash
pytest tests/ -v --cov=src --cov-report=html
```

## Configuration

1. Installer les dépendances :
```bash
pip install -r requirements/dev.txt
```

2. Configurer l'environnement :
```bash
python -c "from database.models import create_tables; create_tables()"
```

## Rapport de Tests

- Rapport HTML : `coverage-report/index.html`
- Rapport XML : `test-results.xml`
- Rapport de couverture : `coverage.xml`