Assistant Virtuel pour l'Immigration Canadienne
Description du Projet
Ce projet est un assistant virtuel pour l'immigration canadienne, développé avec Streamlit. Il offre aux utilisateurs les fonctionnalités suivantes :

Création et gestion de profils personnalisés

Suggestions de visas adaptées à leur situation

Capacité à poser des questions sur les procédures d'immigration

Accès à des ressources officielles

Sauvegarde de l'historique des conversations

L'application combine plusieurs composants clés :

Une base de connaissances structurée sur l'immigration canadienne

Un moteur de conversation intelligent (basé sur OpenAI GPT)

Un système de persistance des données

Des algorithmes de recommandation personnalisés

Classes Principales
1. UserProfile (models.py)
Responsabilité : Représenter les données d'un utilisateur.

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

Stockage des informations démographiques (âge, nationalité, destination, type de profil, fonds).

Gestion de l'historique des conversations.

Méthodes de sérialisation pour la persistance des données.

2. Conversation (models.py)
Responsabilité : Gérer les échanges entre l'utilisateur et l'assistant.

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

Historique chronologique des messages.

Métadonnées de temporisation pour chaque message.

Structure uniforme des messages pour une persistance facile.

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

Gestion centralisée des profils utilisateur et des conversations.

Sérialisation et désérialisation des données au format JSON.

Système de génération d'ID uniques (ex: USER_20250731124500).

4. ImmigrationAgent (immigration_agent.py)
Responsabilité : Contenir la logique métier liée à l'immigration.

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

Intègre une base de connaissances complète sur les visas (critères d'éligibilité, documents requis, délais de traitement).

Implémente des algorithmes de recommandation pour suggérer les options de visa les plus adaptées.

Permet la vérification d'éligibilité basée sur le profil utilisateur.

Fournit un accès aux ressources officielles.

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

Détection d'intention (ex: salutations, questions sur les documents, demandes de visa).

Extraction d'entités (ex: types de visa, destinations spécifiques).

Intégration avec OpenAI GPT pour des réponses contextuelles et intelligentes.

Prise en compte du contexte personnalisé basé sur le profil utilisateur.

Flux d'Exécution Principal (app.py)
Initialisation
Les singletons (instances de DataManager, ImmigrationAgent, ConversationEngine) sont créés et stockés dans st.session_state pour maintenir leur état à travers les rechargements de page.

Les données utilisateur et les conversations existantes sont chargées au démarrage de l'application.

Interface Utilisateur
Une barre latérale (Sidebar) est utilisée pour la gestion des profils (création, sélection) et l'affichage de suggestions de visas personnalisées.

La zone centrale de l'application est dédiée au chat interactif, affichant l'historique des conversations et permettant à l'utilisateur de saisir de nouvelles requêtes.

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
Les données sont sauvegardées automatiquement après chaque interaction significative (ex: envoi d'un message, mise à jour de profil).

L'historique des conversations et les profils sont chargés au redémarrage de l'application, assurant une continuité pour l'utilisateur.

Base de Connaissances (KNOWLEDGE_BASE)
La base de connaissances est une structure hiérarchique qui contient toutes les informations pertinentes sur l'immigration canadienne.

Structure typique :

{
  "visas": [
    {
      "type": "Permis d'études",
      "description": "Permet aux citoyens étrangers d'étudier dans des établissements d'enseignement désignés au Canada.",
      "eligibility": {
        "fonds": "Preuve de fonds suffisants pour couvrir les frais de scolarité, de subsistance et de transport.",
        "langue": "Niveau B2 ou équivalent dans l'une des langues officielles (français ou anglais), sauf exemption.",
        "lettre_acceptation": "Lettre d'acceptation d'un établissement d'enseignement désigné (EED).",
        "casier_judiciaire": "Absence de casier judiciaire."
      },
      "documents_requis": [
        "Passeport valide",
        "Lettre d'acceptation de l'EED",
        "Preuve de fonds",
        "Certificat d'acceptation du Québec (CAQ) si études au Québec",
        "Résultats de test de langue (si applicable)"
      ],
      "processing_time": "Variable (ex: 12 semaines, selon le pays de résidence)",
      "official_links": [
        "https://www.canada.ca/fr/immigration-refugies-citoyennete/services/etudier-canada/permis-etudes.html",
        "https://www.canada.ca/fr/immigration-refugies-citoyennete/services/etudier-canada/permis-etudes/demander.html"
      ]
    },
    {
      "type": "Permis de travail ouvert",
      "description": "Permet de travailler pour n'importe quel employeur au Canada.",
      "eligibility": {
        "programme_specific": "Éligibilité via un programme spécifique (ex: PVT, époux de travailleur/étudiant)",
        "fonds": "Preuve de fonds (selon le programme)",
        "casier_judiciaire": "Absence de casier judiciaire."
      },
      "processing_time": "Variable",
      "official_links": [
        "https://www.canada.ca/fr/immigration-refugies-citoyennete/services/travailler-canada/permis-travail/ouvert.html"
      ]
    },
    {
      "type": "Entrée Express",
      "description": "Système de gestion des demandes d'immigration pour les travailleurs qualifiés.",
      "eligibility": {
        "crs_score": "Score suffisant au Système de Classement Global (CRS).",
        "experience_travail": "Expérience de travail qualifiée.",
        "langue": "Niveau de compétence linguistique élevé."
      },
      "processing_time": "Généralement 6 mois ou moins",
      "official_links": [
        "https://www.canada.ca/fr/immigration-refugies-citoyennete/services/immigrer-canada/entree-express.html",
        "https://www.canada.ca/fr/immigration-refugies-citoyennete/services/immigrer-canada/entree-express/calculer-points-scg.html"
      ]
    }
  ],
  "exigences_linguistiques": {
    "ielts": "Informations sur les scores IELTS requis.",
    "celpip": "Informations sur les scores CELPIP requis."
  },
  "procedures_biometriques": "Détails sur la collecte des données biométriques.",
  "liens_officiels": {
    "ircc": "Lien vers le site officiel d'Immigration, Réfugiés et Citoyenneté Canada (IRCC).",
    "calculateur_crs": "Lien vers le calculateur de score CRS."
  }
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

Ce projet illustre une application complète combinant :

Une interface utilisateur interactive et conviviale (grâce à Streamlit).

Des capacités de traitement du langage naturel pour comprendre et répondre aux requêtes.

Un système de recommandation personnalisé pour guider les utilisateurs.

Une gestion de données persistantes pour une expérience utilisateur continue.

Une intégration puissante avec l'API OpenAI pour une intelligence conversationnelle avancée.
