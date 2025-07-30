# models.py
from datetime import datetime


class UserProfile:
    def _init_(self, user_id, age=None, nationality=None, destination=None, profile_type=None, language_score=None, funds=None):
        self.user_id = user_id
        self.age = age
        self.nationality = nationality
        self.destination = destination
        self.profile_type = profile_type
        self.language_score = language_score
        self.funds = funds
        self.conversations = {}  # Dictionnaire, pas une liste
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "age": self.age,
            "nationality": self.nationality,
            "destination": self.destination,
            "profile_type": self.profile_type,
            "language_score": self.language_score,
            "funds": self.funds,
            # Ne sauvegardez pas les conversations ici - elles seront gérées séparément
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def update_profile(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()


class Conversation:
    def _init_(self, conversation_id, user_id):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.messages = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.status = "active"

    def add_message(self, content, is_user=True):
        message = {
            "id": len(self.messages) + 1,
            "content": content,
            "is_user": is_user,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message

    def to_dict(self):
        return {
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "message_count": len(self.messages),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status
        }