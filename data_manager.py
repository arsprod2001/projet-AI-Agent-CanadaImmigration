import json
import os
from datetime import datetime
from models import UserProfile, Conversation


class DataManager:
    def __init__(self):
        self.users = {}
        self.conversations = {}
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

    def _generate_id(self, prefix):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"{prefix}_{timestamp}"

    def create_user(self, **kwargs):
        user_id = self._generate_id("USER")
        user = UserProfile(user_id, **kwargs)
        self.users[user_id] = user
        self.save_data()
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def create_conversation(self, user_id):
        conv_id = self._generate_id("CONV")
        conversation = Conversation(conv_id, user_id)
        self.conversations[conv_id] = conversation

        user = self.get_user(user_id)
        if user:
            user.conversations[conv_id] = conversation

        self.save_data()
        return conversation

    def save_data(self):
        # Sauvegarde des utilisateurs
        users_data = {uid: user.to_dict() for uid, user in self.users.items()}
        with open(os.path.join(self.data_dir, "users.json"), "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)

        # Sauvegarde des conversations
        conv_data = {cid: conv.to_dict() for cid, conv in self.conversations.items()}
        with open(os.path.join(self.data_dir, "conversations.json"), "w", encoding="utf-8") as f:
            json.dump(conv_data, f, ensure_ascii=False, indent=2)

        # Sauvegarde des messages
        messages_data = {}
        for cid, conv in self.conversations.items():
            messages_data[cid] = conv.messages
        with open(os.path.join(self.data_dir, "messages.json"), "w", encoding="utf-8") as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        def safe_load_json(file_path):
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        try:
                            return json.loads(content)
                        except json.JSONDecodeError:
                            print(f"⚠️ Fichier JSON invalide ignoré : {file_path}")
            return {}

        # Chargement des utilisateurs
        users_file = os.path.join(self.data_dir, "users.json")
        users_data = safe_load_json(users_file)
        for uid, data in users_data.items():
            user = UserProfile(uid)
            for key, value in data.items():
                if key == "conversations":
                    continue
                if key in ["created_at", "updated_at"]:
                    value = datetime.fromisoformat(value)
                setattr(user, key, value)
            self.users[uid] = user

        # Chargement des conversations
        conv_file = os.path.join(self.data_dir, "conversations.json")
        conv_data = safe_load_json(conv_file)
        for cid, data in conv_data.items():
            conv = Conversation(cid, data["user_id"])
            conv.created_at = datetime.fromisoformat(data["created_at"])
            conv.updated_at = datetime.fromisoformat(data["updated_at"])
            conv.status = data["status"]
            self.conversations[cid] = conv

            user_id = data["user_id"]
            if user_id in self.users:
                if not hasattr(self.users[user_id], 'conversations'):
                    self.users[user_id].conversations = {}
                self.users[user_id].conversations[cid] = conv

        # Chargement des messages
        msg_file = os.path.join(self.data_dir, "messages.json")
        msg_data = safe_load_json(msg_file)
        for cid, messages in msg_data.items():
            if cid in self.conversations:
                self.conversations[cid].messages = messages
