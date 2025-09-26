#!/usr/bin/env python3
"""Tests pytest de la base de données"""

import pytest
from datetime import datetime
from pathlib import Path
import sys

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from database.models import PredictionFeedback, Base, engine, SessionLocal
from sqlalchemy.orm import Session

@pytest.fixture(scope="function")
def test_db():
    """Crée une base de données de test temporaire"""
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    
    # Créer une session de test
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Nettoyer après les tests
        Base.metadata.drop_all(bind=engine)

def test_create_feedback(test_db: Session):
    """Test la création d'un feedback"""
    feedback = PredictionFeedback(
        feedback_value=True,
        prediction_result="Cat",
        user_input="test_image.jpg"
    )
    test_db.add(feedback)
    test_db.commit()
    test_db.refresh(feedback)
    
    assert feedback.id is not None
    assert feedback.feedback_value is True
    assert feedback.prediction_result == "Cat"
    assert feedback.user_input == "test_image.jpg"
    assert isinstance(feedback.date, datetime)

def test_query_feedback(test_db: Session):
    """Test la requête de feedback"""
    # Créer plusieurs feedbacks
    feedbacks = [
        PredictionFeedback(feedback_value=True, prediction_result="Cat"),
        PredictionFeedback(feedback_value=False, prediction_result="Dog"),
        PredictionFeedback(feedback_value=True, prediction_result="Cat")
    ]
    test_db.add_all(feedbacks)
    test_db.commit()
    
    # Requêtes de test
    cat_count = test_db.query(PredictionFeedback).filter_by(prediction_result="Cat").count()
    positive_count = test_db.query(PredictionFeedback).filter_by(feedback_value=True).count()
    
    assert cat_count == 2
    assert positive_count == 2

def test_delete_feedback(test_db: Session):
    """Test la suppression de feedback"""
    feedback = PredictionFeedback(
        feedback_value=True,
        prediction_result="Cat"
    )
    test_db.add(feedback)
    test_db.commit()
    
    feedback_id = feedback.id
    test_db.delete(feedback)
    test_db.commit()
    
    deleted = test_db.query(PredictionFeedback).filter_by(id=feedback_id).first()
    assert deleted is None