#!/usr/bin/env python3
"""
Script de démonstration du monitoring
Lance le serveur et ajoute quelques métriques de test
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

def demo_monitoring():
    """Démonstration du système de monitoring"""
    try:
        from src.monitoring.advanced_metrics import log_inference_time, log_feedback_metrics

        print("🚀 Démonstration du système de monitoring")
        print("=" * 50)

        # Simuler des métriques d'inférence variées
        print("📊 Génération de métriques d'inférence...")

        test_data = [
            (120.5, True, "Dog", 0.89, 256000),
            (95.2, True, "Cat", 0.94, 189000),
            (180.3, True, "Dog", 0.76, 320000),
            (450.8, False, None, None, 2048000),  # Erreur
            (135.7, True, "Cat", 0.87, 145000),
            (98.4, True, "Dog", 0.91, 278000),
            (210.1, True, "Cat", 0.83, 367000),
            (75.9, True, "Dog", 0.96, 123000),
        ]

        for i, (time_ms, success, pred, conf, size) in enumerate(test_data):
            log_inference_time(
                inference_time_ms=time_ms,
                success=success,
                prediction=pred,
                confidence=conf,
                file_size_bytes=size
            )
            print(f"   ✅ Requête {i+1}/8 enregistrée")

        # Simuler des feedbacks
        print("\n💬 Génération de métriques de feedback...")

        feedback_data = [
            ("oui", "Dog", "dog_test1.jpg"),
            ("oui", "Cat", "cat_test1.jpg"),
            ("non", "Dog", "wrong_dog.jpg"),
            ("oui", "Cat", "cat_test2.jpg"),
            ("non", "Cat", "wrong_cat.jpg"),
            ("oui", "Dog", "dog_test2.jpg"),
        ]

        for i, (feedback, pred, filename) in enumerate(feedback_data):
            log_feedback_metrics(
                feedback_value=feedback,
                prediction_result=pred,
                user_input=filename
            )
            print(f"   ✅ Feedback {i+1}/6 enregistré")

        print("\n🎉 Données de démonstration générées !")
        print("\n📊 Pour voir le dashboard :")
        print("   1. Lancez le serveur : python scripts/run_api.py")
        print("   2. Ouvrez : http://localhost:8000/monitoring")
        print("\n🔗 API directe : http://localhost:8000/api/monitoring")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_monitoring()