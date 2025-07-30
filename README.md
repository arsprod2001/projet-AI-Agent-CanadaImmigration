Assistant Virtuel pour l'Immigration Canadienne
Description du Projet
Ce projet est un assistant virtuel pour l'immigration canadienne, développé avec Streamlit. Il permet aux utilisateurs de gérer des profils, obtenir des suggestions de visas, poser des questions sur les procédures, consulter des ressources officielles et sauvegarder l'historique des conversations.

L'application combine une base de connaissances structurée, un moteur de conversation intelligent (OpenAI GPT), un système de persistance des données et des algorithmes de recommandation personnalisés.

Classes Principales
1. UserProfile (models.py)
Responsabilité : Gérer les données et l'historique des conversations d'un utilisateur.

class UserProfile:
    def __init__(self, user_id, age, nationality, destination, profile_type, funds):
        self.user_id = user_id
        self.age = age
        self.nationality = nationality
        self.destination = destination
        self.profile_type = profile_type  # étudiant/travailleur/visiteur
        self.funds = funds
        self.conversations = {}  # Historique des conversations

Fonctionnalités clés :

Stockage des informations démographiques.

Gestion de l'historique des conversations et sérialisation pour la persistance.

2. Conversation (models.py)
Responsabilité : Gérer les échanges utilisateur-assistant.

from datetime import datetime

class Conversation:
    def __init__(self, conversation_id, user_id):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.messages = []  # Liste des messages

    def add_message(self, content, is_user):
        self.messages.append({
            "content": content,
            "is_user": is_user,
            "timestamp": datetime.now()
        })

Fonctionnalités clés :

Historique chronologique des messages avec métadonnées.

Structure uniforme pour la persistance.

3. DataManager (data_manager.py)
Responsabilité : Assurer la persistance des données utilisateur.

class DataManager:
    def __init__(self):
        self.users = {}
        self.conversations = {}

    def create_user(self, user_id, **kwargs):
        # Génère un ID unique et crée le profil
        user = UserProfile(user_id, **kwargs)
        self.users[user_id] = user
        return user

    def save_data(self):
        # Sauvegarde en JSON dans /data (implémentation détaillée non montrée)
        pass # Placeholder pour la logique de sauvegarde

Fonctionnalités clés :

Gestion centralisée des profils et conversations.

Sérialisation/désérialisation JSON et système d'ID uniques.

4. ImmigrationAgent (immigration_agent.py)
Responsabilité : Gérer la logique métier de l'immigration.

# KNOWLEDGE_BASE serait importé ou défini ailleurs
KNOWLEDGE_BASE = {
    "visas": [
        {"type": "Permis d'études", "eligibility": {"fonds": "Preuve de fonds suffisants", "langue": "Niveau B2"}, "processing_time": "12 semaines"},
        # ... autres types de visas
    ]
}

class ImmigrationAgent:
    def __init__(self):
        self.knowledge = KNOWLEDGE_BASE  # Base de données structurée

    def suggest_visa_options(self, user_profile):
        suggestions = []
        # Algorithme de matching profil-visa
        for visa in self.knowledge["visas"]:
            # Placeholder pour la logique de calcul de score
            # calcul_match_score(user_profile, visa)
            suggestions.append(visa) # Exemple simple
        return suggestions

    def get_official_resources(self, query):
        # Logique pour trouver des liens officiels pertinents
        return ["https://www.canada.ca/fr/immigration-refugies-citoyennete.html"]

Fonctionnalités clés :

Base de connaissances sur les visas et algorithmes de recommandation.

Vérification d'éligibilité et accès aux ressources officielles.

5. ConversationEngine (conversation_engine.py)
Responsabilité : Gérer les interactions intelligentes et générer les réponses.

# Supposons que 'openai' est configuré
# from openai import OpenAI
# client = OpenAI()

class ConversationEngine:
    def __init__(self, agent):
        self.agent = agent  # Référence à ImmigrationAgent
        self.setup_keywords()  # Configuration NLP (ex: mots-clés, patterns)

    def setup_keywords(self):
        # Configuration simple pour la détection d'intention
        self.greetings = ["bonjour", "salut", "hello"]
        self.visa_queries = ["visa", "permis", "immigration"]

    def detect_intent(self, query):
        query_lower = query.lower()
        if any(g in query_lower for g in self.greetings):
            return "greeting"
        if any(v in query_lower for v in self.visa_queries):
            return "visa_query"
        return "general_query"

    def extract_entities(self, query):
        # Logique d'extraction d'entités (simplifié)
        entities = {}
        if "études" in query.lower():
            entities["type_visa"] = "Permis d'études"
        return entities

    def generate_openai_response(self, query, user, entities):
        # Appel à l'API OpenAI (simplifié)
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "Vous êtes un assistant d'immigration canadien."},
        #         {"role": "user", "content": query}
        #     ]
        # )
        # return response.choices[0].message.content
        return f"Je comprends que vous avez une question sur l'immigration. Pourriez-vous préciser ? (Entités détectées: {entities})"

    def generate_response(self, query, user):
        intent = self.detect_intent(query)  # Classification
        entities = self.extract_entities(query)  # Extraction
        
        if intent == "greeting":
            return "Bonjour ! Comment puis-je vous aider aujourd'hui concernant votre projet d'immigration au Canada ?"
        elif intent == "visa_query":
            # Exemple d'appel à l'agent d'immigration
            if "type_visa" in entities:
                return f"Vous vous intéressez au {entities['type_visa']}? Je peux vous donner des informations sur ce visa."
            return self.generate_openai_response(query, user, entities)
        else:
            return self.generate_openai_response(query, user, entities)

Fonctionnalités clés :

Détection d'intention et extraction d'entités.

Intégration OpenAI GPT et gestion du contexte personnalisé.

Flux d'Exécution Principal (app.py)
Initialisation
Les singletons sont créés et stockés dans st.session_state, et les données existantes sont chargées.

Interface Utilisateur
Une barre latérale gère les profils et suggestions, tandis que la zone centrale affiche le chat interactif.

Gestion des Conversations
import streamlit as st
# Supposons que data_manager, conversation_engine, etc. sont importés et initialisés

# Exemple simplifié de gestion de l'entrée utilisateur
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = data_manager.create_user("temp_user_id", age=30, nationality="FR", destination="CA", profile_type="travailleur", funds=10000)

# if 'conversation_history' not in st.session_state:
#     st.session_state.conversation_history = []

# if prompt := st.chat_input("Posez votre question ici..."):
#     # 1. Ajoute le message utilisateur à l'historique
#     st.session_state.conversation_history.append({"role": "user", "content": prompt})
    
#     # 2. Génère la réponse via ConversationEngine
#     # response = conversation_engine.generate_response(prompt, st.session_state.current_user)
#     response = "Ceci est une réponse simulée." # Placeholder
    
#     # 3. Ajoute la réponse de l'assistant à l'historique
#     st.session_state.conversation_history.append({"role": "assistant", "content": response})
    
#     # 4. Sauvegarde l'échange (via DataManager)
#     # data_manager.save_data() # Appel réel

Persistance
Les données sont sauvegardées automatiquement après chaque interaction et chargées au redémarrage.

Base de Connaissances (KNOWLEDGE_BASE)
Structure hiérarchique contenant des informations sur les visas, exigences linguistiques, procédures biométriques et liens officiels.

Structure typique (exemple simplifié) :

{
  "visas": [
    {
      "type": "Permis d'études",
      "eligibility": {"fonds": "Preuve de fonds suffisants", "langue": "Niveau B2"},
      "processing_time": "12 semaines",
      "official_links": ["https://www.canada.ca/fr/immigration-refugies-citoyennete.html"]
    }
  ],
  "exigences_linguistiques": {"ielts": "Scores requis"},
  "liens_officiels": {"ircc": "Site officiel"}
}

Architecture Globale
Streamlit UI (app.py)
│
├── ConversationEngine (NLP/OpenAI)
│   └── ImmigrationAgent (Logique métier)
│       └── KNOWLEDGE_BASE
│
└── DataManager (Persistance)
    ├── UserProfiles
    └── Conversations

Ce projet combine une interface utilisateur interactive, le traitement du langage naturel, un système de recommandation, la gestion de données persistantes et l'intégration OpenAI.
