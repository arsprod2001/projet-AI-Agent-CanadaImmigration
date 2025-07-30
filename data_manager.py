import json
import os
from datetime import datetime
from models import UserProfile, Conversation


class DataManager:
    def _init_(self):
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
        conv_data = {cid: conv.to_dict()
                     for cid, conv in self.conversations.items()}
        with open(os.path.join(self.data_dir, "conversations.json"), "w", encoding="utf-8") as f:
            json.dump(conv_data, f, ensure_ascii=False, indent=2)

        # Sauvegarde des messages
        messages_data = {}
        for cid, conv in self.conversations.items():
            messages_data[cid] = conv.messages
        with open(os.path.join(self.data_dir, "messages.json"), "w", encoding="utf-8") as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        # Chargement des utilisateurs
        users_file = os.path.join(self.data_dir, "users.json")
        if os.path.exists(users_file):
            with open(users_file, "r", encoding="utf-8") as f:
                users_data = json.load(f)
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
        if os.path.exists(conv_file):
            with open(conv_file, "r", encoding="utf-8") as f:
                conv_data = json.load(f)
                for cid, data in conv_data.items():
                    conv = Conversation(cid, data["user_id"])
                    conv.created_at = datetime.fromisoformat(
                        data["created_at"])
                    conv.updated_at = datetime.fromisoformat(
                        data["updated_at"])
                    conv.status = data["status"]
                    self.conversations[cid] = conv

                    user_id = data["user_id"]
                    if user_id in self.users:
                        if not hasattr(self.users[user_id], 'conversations'):
                            self.users[user_id].conversations = {}
                        self.users[user_id].conversations[cid] = conv

        # Chargement des messages
        msg_file = os.path.join(self.data_dir, "messages.json")
        if os.path.exists(msg_file):
            with open(msg_file, "r", encoding="utf-8") as f:
                msg_data = json.load(f)
                for cid, messages in msg_data.items():
                    if cid in self.conversations:
                        self.conversations[cid].messages = messages