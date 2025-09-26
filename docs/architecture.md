# Architecture du Projet Cats vs Dogs Classifier

## Vue d'ensemble

L'application est une solution complète de classification d'images utilisant le deep learning, avec une interface web et un système de feedback utilisateur. Voici les principaux composants :

```mermaid
graph TB
    subgraph Frontend ["Interface Utilisateur"]
        Web["Interface Web"]
        Templates["Templates Jinja2"]
    end

    subgraph Backend ["Backend FastAPI"]
        API["API REST"]
        Auth["Authentification"]
        Routes["Routes"]
    end

    subgraph ML ["Machine Learning"]
        Model["Modèle TensorFlow"]
        Predictor["Prédicteur"]
    end

    subgraph Storage ["Stockage"]
        DB[(Base de données SQLite)]
        CSV["Métriques CSV"]
    end

    subgraph Monitoring ["Monitoring"]
        Metrics["Métriques d'inférence"]
        Feedback["Feedback utilisateur"]
    end

    Web -->|HTTP| API
    API --> Auth
    Auth --> Routes
    Routes --> Predictor
    Predictor --> Model
    Routes -->|Enregistre| DB
    Routes -->|Log| CSV
    Metrics -->|Analyse| CSV
    Feedback -->|Stocke| DB

    style Frontend fill:#f9f,stroke:#333,stroke-width:2px
    style Backend fill:#bbf,stroke:#333,stroke-width:2px
    style ML fill:#bfb,stroke:#333,stroke-width:2px
    style Storage fill:#fbb,stroke:#333,stroke-width:2px
    style Monitoring fill:#ffb,stroke:#333,stroke-width:2px
```

## Structure des Dossiers

```
computer-vision-cats-and-dogs/
├── src/
│   ├── api/            # API FastAPI
│   ├── models/         # Modèles ML
│   ├── monitoring/     # Monitoring
│   └── web/           # Interface web
├── database/          # Base de données
├── tests/            # Tests automatisés
├── config/           # Configuration
└── docs/            # Documentation
```

## Flux de Données

1. **Soumission d'Image**
   - L'utilisateur soumet une image via l'interface web
   - L'API valide l'authentification et le format
   - Le prédicteur traite l'image
   - Le résultat est renvoyé à l'utilisateur

2. **Feedback Utilisateur**
   - L'utilisateur donne son feedback (correct/incorrect)
   - Le feedback est stocké dans la base SQLite
   - Les métriques sont mises à jour

3. **Monitoring**
   - Le temps d'inférence est enregistré
   - Les métriques de performance sont suivies
   - Les données de feedback sont analysées

## Technologies Utilisées

- **Frontend** : HTML, JavaScript, Bootstrap
- **Backend** : FastAPI, Python
- **ML** : TensorFlow, Keras
- **Base de données** : SQLite, SQLAlchemy
- **Monitoring** : CSV, Métriques personnalisées
- **Tests** : Pytest
- **CI/CD** : GitHub Actions

## Points de Sécurité

- Authentification par token
- Validation des entrées utilisateur
- Filtrage des types de fichiers
- Gestion des erreurs structurée

## Monitoring et Performance

- Temps d'inférence
- Taux de succès des prédictions
- Feedback utilisateur
- Métriques de performance du modèle