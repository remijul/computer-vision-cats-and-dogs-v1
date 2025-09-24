import sys
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, delete

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

print(f"ROOT_DIR ajouté au path: {ROOT_DIR}")

from src.database.db_models import Prediction, Feedback
from src.database.db_engine import engine

class DatabaseOperations:
    """Classe pour gérer les opérations sur la base de données"""
    
    def __init__(self):
        self.engine = engine
    
    # =================== OPÉRATIONS SUR PREDICTION ===================
    
    def create_prediction(self, probabilite_chat: float, image_path: str, 
                         inference_time_ms: float, date_prediction: Optional[datetime] = None) -> Prediction:
        """
        Créer une nouvelle prédiction dans la base de données
        
        Args:
            probabilite_chat: Probabilité que ce soit un chat (entre 0 et 1)
            image_path: Chemin vers l'image
            inference_time_ms: Temps d'inférence en millisecondes
            date_prediction: Date de la prédiction (par défaut aujourd'hui)
        
        Returns:
            L'objet Prediction créé
        """
        with Session(self.engine) as session:
            if date_prediction is None:
                date_prediction = datetime.now()
            
            prediction = Prediction(
                date_prediction=date_prediction,
                probabilite_chat=probabilite_chat,
                image_path=image_path,
                inference_time_ms=inference_time_ms
            )
            
            session.add(prediction)
            session.commit()
            session.refresh(prediction)  # Pour récupérer l'ID généré
            print(f"Prédiction créée avec l'ID: {prediction.id_predict}")
            return prediction
    
    def get_prediction_by_id(self, prediction_id: int) -> Optional[Prediction]:
        """
        Récupérer une prédiction par son ID
        
        Args:
            prediction_id: L'ID de la prédiction
        
        Returns:
            L'objet Prediction ou None si non trouvé
        """
        with Session(self.engine) as session:
            prediction = session.get(Prediction, prediction_id)
            if prediction:
                print(f"Prédiction trouvée: ID={prediction.id_predict}, Chat={prediction.probabilite_chat}")
            else:
                print(f"Aucune prédiction trouvée avec l'ID: {prediction_id}")
            return prediction
    
    def get_all_predictions(self) -> List[Prediction]:
        """
        Récupérer toutes les prédictions
        
        Returns:
            Liste de toutes les prédictions
        """
        with Session(self.engine) as session:
            statement = select(Prediction)
            predictions = session.exec(statement).all()
            print(f"{len(predictions)} prédiction(s) trouvée(s)")
            return predictions
    
    def update_prediction(self, prediction_id: int, **kwargs) -> Optional[Prediction]:
        """
        Mettre à jour une prédiction
        
        Args:
            prediction_id: ID de la prédiction à modifier
            **kwargs: Les champs à modifier (probabilite_chat, image_path, inference_time_ms, etc.)
        
        Returns:
            La prédiction modifiée ou None si non trouvée
        """
        with Session(self.engine) as session:
            prediction = session.get(Prediction, prediction_id)
            if not prediction:
                print(f"Prédiction avec ID {prediction_id} non trouvée")
                return None
            
            # Mettre à jour les champs fournis
            for key, value in kwargs.items():
                if hasattr(prediction, key):
                    setattr(prediction, key, value)
                    print(f"Champ {key} mis à jour: {value}")
            
            session.add(prediction)
            session.commit()
            session.refresh(prediction)
            print(f"Prédiction {prediction_id} mise à jour avec succès")
            return prediction
    
    def delete_prediction(self, prediction_id: int) -> bool:
        """
        Supprimer une prédiction
        
        Args:
            prediction_id: ID de la prédiction à supprimer
        
        Returns:
            True si supprimé avec succès, False sinon
        """
        with Session(self.engine) as session:
            prediction = session.get(Prediction, prediction_id)
            if not prediction:
                print(f"Prédiction avec ID {prediction_id} non trouvée")
                return False
            
            session.delete(prediction)
            session.commit()
            print(f"Prédiction {prediction_id} supprimée avec succès")
            return True
    
    # =================== OPÉRATIONS SUR FEEDBACK ===================
    
    def create_feedback(self, prediction_id: int, feedback: bool) -> Optional[Feedback]:
        """
        Créer un nouveau feedback pour une prédiction
        
        Args:
            prediction_id: ID de la prédiction associée
            feedback: True si la prédiction était correcte, False sinon
        
        Returns:
            L'objet Feedback créé ou None si la prédiction n'existe pas
        """
        with Session(self.engine) as session:
            # Vérifier que la prédiction existe
            prediction = session.get(Prediction, prediction_id)
            if not prediction:
                print(f"Prédiction avec ID {prediction_id} non trouvée")
                return None
            
            feedback_obj = Feedback(
                prediction_id=prediction_id,
                feedback=feedback
            )
            
            session.add(feedback_obj)
            session.commit()
            session.refresh(feedback_obj)
            print(f"Feedback créé avec l'ID: {feedback_obj.id}")
            return feedback_obj
    
    def get_feedback_by_id(self, feedback_id: int) -> Optional[Feedback]:
        """
        Récupérer un feedback par son ID
        
        Args:
            feedback_id: L'ID du feedback
        
        Returns:
            L'objet Feedback ou None si non trouvé
        """
        with Session(self.engine) as session:
            feedback = session.get(Feedback, feedback_id)
            if feedback:
                print(f"Feedback trouvé: ID={feedback.id}, Correct={feedback.feedback}")
            else:
                print(f"Aucun feedback trouvé avec l'ID: {feedback_id}")
            return feedback
    
    def get_feedback_by_prediction(self, prediction_id: int) -> Optional[Feedback]:
        """
        Récupérer le feedback d'une prédiction spécifique
        
        Args:
            prediction_id: ID de la prédiction
        
        Returns:
            L'objet Feedback ou None si non trouvé
        """
        with Session(self.engine) as session:
            statement = select(Feedback).where(Feedback.prediction_id == prediction_id)
            feedback = session.exec(statement).first()
            if feedback:
                print(f"Feedback pour prédiction {prediction_id}: {feedback.feedback}")
            else:
                print(f"Aucun feedback pour la prédiction {prediction_id}")
            return feedback
    
    def get_all_feedbacks(self) -> List[Feedback]:
        """
        Récupérer tous les feedbacks
        
        Returns:
            Liste de tous les feedbacks
        """
        with Session(self.engine) as session:
            statement = select(Feedback)
            feedbacks = session.exec(statement).all()
            print(f"{len(feedbacks)} feedback(s) trouvé(s)")
            return feedbacks
    
    def update_feedback(self, feedback_id: int, feedback_value: bool) -> Optional[Feedback]:
        """
        Mettre à jour un feedback
        
        Args:
            feedback_id: ID du feedback à modifier
            feedback_value: Nouvelle valeur du feedback
        
        Returns:
            Le feedback modifié ou None si non trouvé
        """
        with Session(self.engine) as session:
            feedback = session.get(Feedback, feedback_id)
            if not feedback:
                print(f"Feedback avec ID {feedback_id} non trouvé")
                return None
            
            feedback.feedback = feedback_value
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            print(f"Feedback {feedback_id} mis à jour: {feedback_value}")
            return feedback
    
    def delete_feedback(self, feedback_id: int) -> bool:
        """
        Supprimer un feedback
        
        Args:
            feedback_id: ID du feedback à supprimer
        
        Returns:
            True si supprimé avec succès, False sinon
        """
        with Session(self.engine) as session:
            feedback = session.get(Feedback, feedback_id)
            if not feedback:
                print(f"Feedback avec ID {feedback_id} non trouvé")
                return False
            
            session.delete(feedback)
            session.commit()
            print(f"Feedback {feedback_id} supprimé avec succès")
            return True
    
    # =================== MÉTHODES UTILES ===================
    
    def get_prediction_with_feedback(self, prediction_id: int) -> Optional[Prediction]:
        """
        Récupérer une prédiction avec son feedback associé
        
        Args:
            prediction_id: ID de la prédiction
        
        Returns:
            La prédiction avec son feedback chargé
        """
        with Session(self.engine) as session:
            statement = select(Prediction).where(Prediction.id_predict == prediction_id)
            prediction = session.exec(statement).first()
            if prediction and prediction.feedback:
                print(f"Prédiction {prediction_id}: Chat={prediction.probabilite_chat}, "
                      f"Feedback={prediction.feedback.feedback}")
            return prediction
    
    def get_statistics(self) -> dict:
        """
        Obtenir des statistiques simples sur les données
        
        Returns:
            Dictionnaire avec les statistiques
        """
        with Session(self.engine) as session:
            total_predictions = len(session.exec(select(Prediction)).all())
            total_feedbacks = len(session.exec(select(Feedback)).all())
            
            # Compter les feedbacks positifs
            positive_feedbacks = len(session.exec(
                select(Feedback).where(Feedback.feedback == True)
            ).all())
            
            stats = {
                'total_predictions': total_predictions,
                'total_feedbacks': total_feedbacks,
                'positive_feedbacks': positive_feedbacks,
                'negative_feedbacks': total_feedbacks - positive_feedbacks
            }
            
            print("Statistiques de la base de données:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
            
            return stats


# =================== EXEMPLE D'UTILISATION ===================
if __name__ == "__main__":
    # Créer une instance de la classe
    db = DatabaseOperations()
    
    print("=== Test des opérations sur la base de données ===\n")
    
    # Créer une prédiction
    print("1. Création d'une prédiction:")
    prediction = db.create_prediction(
        probabilite_chat=0.85,
        image_path="/images/chat1.jpg",
        inference_time_ms=150.5
    )
    
    # Lire la prédiction
    print("\n2. Lecture de la prédiction:")
    db.get_prediction_by_id(prediction.id_predict)
    
    # Créer un feedback
    print("\n3. Création d'un feedback:")
    feedback = db.create_feedback(prediction.id_predict, True)
    
    # Lire le feedback
    print("\n4. Lecture du feedback:")
    db.get_feedback_by_prediction(prediction.id_predict)
    
    # Afficher les statistiques
    print("\n5. Statistiques:")
    db.get_statistics()
    
    print("\n=== Fin des tests ===")
