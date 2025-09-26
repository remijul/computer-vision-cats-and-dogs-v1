-- Schema de la base de données pour l'application de classification chats/chiens
-- Créé le 25 septembre 2025

-- Table des feedbacks utilisateurs
CREATE TABLE predictions_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Identifiant unique
    feedback_value BOOLEAN,                       -- Valeur du feedback (1=oui/positif, 0=non/négatif)
    date DATETIME DEFAULT CURRENT_TIMESTAMP,      -- Date du feedback
    prediction_result TEXT,                       -- Résultat de la prédiction (chat/chien)
    user_input TEXT,                              -- Input utilisateur (nom du fichier image)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP -- Date de création de l'enregistrement
);

-- Index pour optimiser les requêtes
CREATE INDEX idx_feedback_date ON predictions_feedback(date);
CREATE INDEX idx_feedback_value ON predictions_feedback(feedback_value);
CREATE INDEX idx_prediction_result ON predictions_feedback(prediction_result);

-- Commentaires sur la structure :
-- - feedback_value : boolean (1 pour feedback positif "oui", 0 pour négatif "non")
-- - date : timestamp de quand le feedback a été donné
-- - prediction_result : le résultat que le modèle a prédit (chat ou chien)
-- - user_input : l'input de l'utilisateur (généralement le nom du fichier image)
-- - created_at : timestamp automatique de création de l'enregistrement