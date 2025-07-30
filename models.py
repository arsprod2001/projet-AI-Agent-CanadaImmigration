from datetime import datetime


class UserProfile:
    def __init__(self, user_id, age=None, nationality=None, destination=None, profile_type=None, funds=None):
        self.user_id = user_id
        self.age = age
        self.nationality = nationality
        self.destination = destination
        self.profile_type = profile_type
        self.funds = funds
        self.conversations = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "age": self.age,
            "nationality": self.nationality,
            "destination": self.destination,
            "profile_type": self.profile_type,
            "funds": self.funds,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def update_profile(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()


class Conversation:
    def __init__(self, conversation_id, user_id):
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
