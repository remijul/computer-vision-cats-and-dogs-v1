# Documentation Technique - Cats vs Dogs Classifier

## Table des matières
1. [Vue d'ensemble](#vue-densemble)
2. [Architecture](#architecture)
3. [Composants](#composants)
4. [Flux de données](#flux-de-données)
5. [Technologies](#technologies)
6. [Installation](#installation)
7. [Utilisation](#utilisation)
8. [Maintenance](#maintenance)

## Vue d'ensemble

Le projet "Cats vs Dogs Classifier" est une application web qui permet de classifier des images de chats et de chiens en utilisant l'intelligence artificielle. L'application offre :

- Une interface web intuitive
- Un système de classification d'images en temps réel
- Un mécanisme de feedback utilisateur
- Un système de monitoring des performances

## Architecture

L'application est construite selon une architecture moderne en couches :

![Architecture générale](img/architecture.png)

L'application se compose de trois parties principales :
1. **Frontend** : Interface utilisateur web
2. **Backend** : API REST avec FastAPI
3. **ML** : Modèle de classification TensorFlow

## Composants

### 1. Interface Utilisateur
![Interface](img/interface.png)

L'interface permet aux utilisateurs de :
- Télécharger des images
- Voir les prédictions en temps réel
- Donner leur feedback
- Consulter les statistiques

### 2. API Backend
L'API REST gère :
- La réception des images
- L'authentification
- Les prédictions
- Le stockage des données

### 3. Modèle ML
Le modèle de deep learning :
- Utilise TensorFlow/Keras
- Est pré-entraîné sur des milliers d'images
- Donne des prédictions avec score de confiance

## Flux de données

![Flux de données](img/workflow.png)

1. **Soumission d'image**
   - L'utilisateur soumet une image
   - L'API valide le format
   - Le modèle fait une prédiction
   - Le résultat est affiché

2. **Feedback**
   - L'utilisateur indique si la prédiction est correcte
   - Le feedback est enregistré en base de données
   - Les métriques sont mises à jour

## Technologies

### Frontend
- HTML5/CSS3
- JavaScript
- Bootstrap 5
- Templates Jinja2

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite

### ML
- TensorFlow 2.x
- Keras
- NumPy
- Pillow

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/Arno37/computer-vision-cats-and-dogs.git
```

2. Créer l'environnement virtuel :
```bash
python -m venv baseenv
source baseenv/bin/activate  # Linux/Mac
baseenv\Scripts\activate.bat  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements/dev.txt
```

## Utilisation

1. Démarrer le serveur :
```bash
python -m uvicorn src.api.main:app --reload
```

2. Ouvrir dans le navigateur :
```
http://localhost:8000
```

3. Pour les tests :
```bash
pytest tests/ -v
```

## Maintenance

### Monitoring
- Temps d'inférence
- Taux de succès
- Feedback utilisateur
- Logs d'erreurs

### Mise à jour
1. Vérifier les dépendances
2. Exécuter les tests
3. Déployer les changements

### Support
Pour toute question :
- Ouvrir une issue sur GitHub
- Contacter l'équipe de maintenance