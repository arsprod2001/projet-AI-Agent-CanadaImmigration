# app.py
import streamlit as st
from data_manager import DataManager
from models import UserProfile
from immigration_agent import ImmigrationAgent
from conversation_engine import ConversationEngine

# Initialisation
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
    st.session_state.data_manager.load_data()

if 'immigration_agent' not in st.session_state:
    st.session_state.immigration_agent = ImmigrationAgent()

if 'conversation_engine' not in st.session_state:
    st.session_state.conversation_engine = ConversationEngine(
        st.session_state.immigration_agent)

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None

# Interface Streamlit
st.title("🤖 Assistant d'Immigration Canadienne")

# Sidebar pour la gestion du profil
with st.sidebar:
    st.header("Gestion du Profil")

    # Création de profil
    with st.expander("Créer un Profil"):
        with st.form("profile_form"):
            age = st.number_input("Âge", min_value=1, max_value=100, step=1)
            nationality = st.text_input("Nationalité")
            destination = st.text_input("Destination (Province)")
            profile_type = st.selectbox(
                "Type de profil", ["", "étudiant", "travailleur", "visiteur"])
            funds = st.number_input(
                "Fonds disponibles ($ CAD)", min_value=0.0, step=1000.0)
            submit_profile = st.form_submit_button("Créer le Profil")

            if submit_profile:
                if not profile_type:
                    st.error("Veuillez sélectionner un type de profil")
                else:
                    user = st.session_state.data_manager.create_user(
                        age=age,
                        nationality=nationality,
                        destination=destination,
                        profile_type=profile_type,
                        funds=funds
                    )
                    st.session_state.current_user = user
                    st.success(f"Profil créé avec ID: {user.user_id}")

    # Charger un profil existant avec historique
    with st.expander("Charger un Profil Existant"):
        user_ids = list(st.session_state.data_manager.users.keys())
        selected_user = st.selectbox("Sélectionnez un profil", user_ids)
        if st.button("Charger le Profil"):
            user = st.session_state.data_manager.get_user(selected_user)
            st.session_state.current_user = user

            # Charger la dernière conversation du profil
            if hasattr(user, 'conversations') and user.conversations:
                conv_ids = sorted(user.conversations.keys())
                latest_conv_id = conv_ids[-1]
                st.session_state.current_conversation = user.conversations[latest_conv_id]

                # Afficher l'historique dans la zone de conversation
                st.session_state.messages = []
                for msg in st.session_state.current_conversation.messages:
                    role = "user" if msg['is_user'] else "assistant"
                    st.session_state.messages.append({
                        "role": role,
                        "content": msg['content']
                    })
            else:
                st.session_state.current_conversation = None
                st.session_state.messages = []

            st.success(f"Profil {selected_user} chargé")
            st.rerun()

    # Afficher le profil actuel
    if st.session_state.current_user:
        st.subheader("Profil Actuel")
        user = st.session_state.current_user
        st.write(f"ID: {user.user_id}")
        st.write(f"Âge: {user.age}")
        st.write(f"Nationalité: {user.nationality}")
        st.write(f"Destination: {user.destination}")
        st.write(f"Type: {user.profile_type}")
        st.write(f"Fonds: {user.funds} $ CAD")

    # Suggestions de visas
    if st.button("Obtenir des Suggestions de Visas"):
        if st.session_state.current_user:
            suggestions = st.session_state.immigration_agent.suggest_visa_options(
                st.session_state.current_user)
            if suggestions:
                st.subheader("Suggestions de Visas")
                for i, visa in enumerate(suggestions[:3], 1):
                    st.write(
                        f"{i}. **{visa['type']}** - Adéquation: {visa['match_score']}%")
                    st.caption(visa['description'])
            else:
                st.warning("Aucune suggestion disponible pour votre profil")
        else:
            st.warning("Veuillez d'abord créer ou charger un profil")

    # Ressources
    st.subheader("Ressources Utiles")
    resources = st.session_state.immigration_agent.get_official_resources()
    for name, url in resources.items():
        st.markdown(f"[{name}]({url})")

# Zone de conversation
st.header("💬 Conversation")

# Avertissement si pas de profil
if not st.session_state.current_user:
    st.warning(
        "⚠️ Créez ou chargez un profil dans la barre latérale pour personnaliser les réponses.")

# Initialiser l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestion de la saisie utilisateur
if prompt := st.chat_input("Posez votre question sur l'immigration canadienne..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not st.session_state.current_conversation and st.session_state.current_user:
        st.session_state.current_conversation = st.session_state.data_manager.create_conversation(
            st.session_state.current_user.user_id
        )

    response = st.session_state.conversation_engine.generate_response(
        prompt,
        st.session_state.current_user
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    if st.session_state.current_conversation:
        st.session_state.current_conversation.add_message(prompt, is_user=True)
        st.session_state.current_conversation.add_message(
            response, is_user=False)
        st.session_state.data_manager.save_data()

# Commandes rapides
st.subheader("Commandes Rapides")
col1, col2 = st.columns(2)
with col1:
    if st.button("Afficher les types de visas"):
        prompt = "Quels sont les types de visas disponibles ?"
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        visa_types = st.session_state.immigration_agent.get_visa_types()
        response = "Voici les types de visas disponibles :\n" + \
            "\n".join(f"- {vt}" for vt in visa_types)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

        if st.session_state.current_conversation:
            st.session_state.current_conversation.add_message(
                prompt, is_user=True)
            st.session_state.current_conversation.add_message(
                response, is_user=False)
            st.session_state.data_manager.save_data()

        st.rerun()

with col2:
    if st.button("Réinitialiser la conversation"):
        st.session_state.messages = []
        st.rerun()
