# conversation_engine.py
import openai
import os
from dotenv import load_dotenv

# Charger la clé API depuis .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class ConversationEngine:
    def __init__(self, agent):
        self.agent = agent
        self.setup_keywords()

    def setup_keywords(self):
        """Configuration des mots-clés et intentions"""
        self.intents = {
            "greeting": ["bonjour", "salut", "coucou", "hello", "hi", "hey", "Mbotte"],
            "goodbye": ["merci", "au revoir", "bye", "à plus", "ciao", "exit", "quitter"],
            "documents": ["document", "papier", "liste", "fournir", "requis", "préparer"],
            "délais": ["délai", "temps", "combien de temps", "durée", "attente", "traiter"],
            "éligibilité": ["éligible", "critère", "condition", "requis", "besoin", "qualifié"],
            "langue": ["langue", "linguistique", "ielts", "tef", "celpip", "test", "niveau"],
            "biométrie": ["biométrie", "empreinte", "photo", "reconnaissance", "biometric"],
            "ressources": ["lien", "site", "officiel", "ressource", "information", "guide"],
            "profil": ["profil", "compte", "informations personnelles", "mes données"],
            "suggestion": ["suggestion", "conseil", "option", "meilleur choix", "recommander"]
        }

        self.visa_types = []
        for v in self.agent.get_visa_types():
            self.visa_types.append(v.lower())

        # Récupération dynamique des types de profil
        try:
            # On essaie d'obtenir les types depuis l'agent
            liste = self.agent.get_profile_types()
            self.profile_types = []
            for p in liste:
                self.profile_types.append(p.lower())
        except AttributeError:
            # Si ça ne marche pas, on utilise une liste fixe par défaut
            self.profile_types = ["étudiant", "travailleur", "résident", "visiteur"]

    def detect_intent(self, query):
        """Détecte l'intention principale de la requête"""
        query_lower = query.lower()

        for intent, keywords in self.intents.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent

        return "unknown"

    def extract_entities(self, query):
        """Extrait les entités importantes de la requête"""
        query_lower = query.lower()
        entities = {
            "visa_type": None,
            "destination": None,
            "profile_type": None
        }

        # Extraction du type de visa
        for visa_type in self.visa_types:
            if visa_type in query_lower:
                entities["visa_type"] = visa_type
                break

        # Extraction de la destination
        if "québec" in query_lower:
            entities["destination"] = "Québec"
        elif "ontario" in query_lower:
            entities["destination"] = "Ontario"
        elif "colombie britannique" in query_lower:
            entities["destination"] = "Colombie-Britannique"

        # Extraction du type de profil
        for p_type in self.profile_types:
            if p_type in query_lower:
                entities["profile_type"] = p_type
                break

        return entities

    def generate_openai_response(self, query, user, entities):
        """Génère une réponse avec contexte enrichi"""
        knowledge_context = self.agent.get_knowledge_context()

        # Contexte utilisateur
        user_context = ""
        if user:
            user_context = (
                f"\n\nProfil utilisateur:"
                f"\n- Âge: {user.age}"
                f"\n- Nationalité: {user.nationality}"
                f"\n- Destination: {user.destination}"
                f"\n- Type de profil: {user.profile_type}"
                f"\n- Fonds disponibles: {user.funds} $ CAD"
            )

        # Contexte des entités extraites
        entities_context = (
            f"\n\nEntités détectées:"
            f"\n- Type de visa: {entities['visa_type'] or 'Non spécifié'}"
            f"\n- Destination: {entities['destination'] or 'Non spécifiée'}"
            f"\n- Type de profil: {entities['profile_type'] or 'Non spécifié'}"
        )

        prompt = (
            "Tu es un assistant expert en immigration canadienne. "
            "Réponds strictement en utilisant les informations de la base de connaissances fournie. "
            "Si l'information n'est pas disponible, indique-le clairement. "
            "\n\n"
            f"{knowledge_context}"
            f"{user_context}"
            f"{entities_context}"
            "\n\n"
            f"Question: {query}"
            "\n\nRéponse:"
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un assistant spécialisé en immigration canadienne."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message['content'].strip()

        except Exception as e:
            return f"Erreur de l'API OpenAI: {str(e)}"

    def generate_response(self, query, user=None):
        """Génère une réponse contextuelle basée sur l'intention et les entités"""
        intent = self.detect_intent(query)
        entities = self.extract_entities(query)

        # Gestion des salutations
        if intent == "greeting":
            if user:
                return f"Bonjour de retour ! Comment puis-je vous aider aujourd'hui ?"
            return "Bonjour ! Je suis votre assistant spécialisé en immigration canadienne. Comment puis-je vous aider ?"

        # Gestion des adieux
        if intent == "goodbye":
            return "Merci d'avoir utilisé nos services ! N'hésitez pas à revenir si vous avez d'autres questions."

        # Gestion du profil utilisateur (CORRIGÉ)
        if intent == "profil" and user:
            return self.handle_profile_request(user)

        # Toutes les autres intentions utilisent OpenAI avec contexte enrichi
        return self.generate_openai_response(query, user, entities)

    # ===== HANDLER PROFIL UTILISATEUR =====
    def handle_profile_request(self, user):
        response = "👤 Votre profil :\n"
        response += f"• ID: {user.user_id}\n"
        response += f"• Âge: {user.age or 'Non spécifié'}\n"
        response += f"• Nationalité: {user.nationality or 'Non spécifiée'}\n"
        response += f"• Destination: {user.destination or 'Non spécifiée'}\n"
        response += f"• Profil: {user.profile_type or 'Non spécifié'}\n"
        response += f"• Fonds disponibles: {user.funds or 'Non spécifié'} $ CAD"
        return response
