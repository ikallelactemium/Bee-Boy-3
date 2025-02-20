import os
import streamlit as st
from openai import AzureOpenAI
from streamlit_star_rating import st_star_rating
import pandas as pd
import json
import base64
import datetime
import config
from utils_user_authentication import *
from streamlit_lottie import st_lottie




# ------------------------------------------------------------------------
# À compléter avec vos informations :
#
#   1. Endpoint Azure OpenAI (URL de l’instance)
#   2. Deployment Name du modèle (ex: gpt-4)
#   3. Clé d'API Azure OpenAI
#   4. Endpoint et clé de votre service Azure Cognitive Search
#   5. Nom de l'index de recherche
# ------------------------------------------------------------------------

# Vous pouvez soit stocker ces infos dans des variables d'environnements,
# soit les définir directement ici (pas recommandé en prod).
endpoint = config.endpoint
deployment =  config.deployment
search_endpoint = config.search_endpoint
search_key = config.search_key
search_index = config.search_index
subscription_key = config.subscription_key


# Mise en page et configuration de la page
st.set_page_config(page_title="Assistant IA", layout="wide")



def info_message_markdown_with_link(url,code_connexion):
    html = """
    <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" >
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <div class="alert alert-primary" role="alert">
    Cliquer <a href="""+ url + """ class="alert-link">ICI</a>, ensuite entrez le code <strong>""" + code_connexion + """</strong> pour vous authentifier
    </div>
    """
    st.markdown(html,unsafe_allow_html=True)


def alerte_message_markdown(message):
    html = """
    <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" >
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <div class="alert alert-danger" role="alert">
    """+ message + """
    </div>
    """
    st.markdown(html,unsafe_allow_html=True)


    
def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
    

if "auth" not in st.session_state :

    if  "connexion_timeout" in st.session_state :  
        col1,col2,col3 = st.columns([1,2,1])
        st.error("Oops! Erreur  : Délai de connexion dépassé , Merci de réactualiser la page", icon="🚨")
        st.stop()


    form_load_beewave = st.form(
        key="my_form_load_beewave", clear_on_submit=True
    )

    st.markdown(
        """
        <style>
        div.row-widget.stButton > button:first-child {
            background-color: black;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    # --- Ajout de CSS pour centrer les widgets ---
    st.markdown("""
        <style>
            .center-lottie {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0 auto;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Création du formulaire ---
    form_load_beewave = st.form(key="form_beewave")

    with form_load_beewave:
        # Charger l'animation Lottie
        lottie_json = load_lottiefile("Animation - 1734366168754.json")
        
        # Encapsuler l'animation dans une div centrée
        st.markdown('<div class="center-lottie">', unsafe_allow_html=True)
        st_lottie(
            lottie_json,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            width=500,
            key="100",
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Bouton de soumission
        load_beewave = form_load_beewave.form_submit_button("**Se connecter à BeeWave**")

    if load_beewave:
        class_user_auth = user_authantification()
        app,flow = class_user_auth.azure_AD_authantification()
        url = flow['verification_uri']
        info_message_markdown_with_link(url,flow['user_code'])
        alerte_message_markdown("Attention : Ce code est valide pendant  15 min")

        try :
            response = user_authantification.send_request(app,flow)
            user_connected = response["displayName"]
            st.session_state["auth"] = user_connected
            st.rerun()
        except Exception as err:
            st.session_state["connexion_timeout"] = "time out"
            st.rerun()



else:











    st.markdown('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)

    st.logo("Actemium.png",link="https://www.actemium.fr/implantations/actemium-maintenance-toulouse/presentation/", icon_image="Actemium.png")

    # Initialisation du client Azure OpenAI
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version="2024-05-01-preview",
    )

    # CSS Amélioré
    st.markdown("""
    <style>
        body {
            background-color: #f4f7fb;
            color: #333;
            font-family: "Segoe UI", sans-serif;
        }
        header, footer {visibility: hidden;}
        h1, h2, h3, h4, h5, h6 {
            color: #004080;
        }
        .stButton>button {
            background-color: #004080;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #003366;
        }
        .stTextInput>div>div>input {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 8px;
            background-color: #fff;
            color: #333;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .chat-message {
            background-color: #ffffff;
            border: 1px solid #e6e6e6;
            padding: 10px;
            margin: 5px 0;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            color: #333;
        }
        .user-message {
            text-align: left;
            background-color: #f0f8ff;
            border: 1px solid #d4e3fc;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            color: #004080;
            box-shadow: none;
        }
        .assistant-message {
            text-align: left;
            background-color: #f9f9f9;
            border: 1px solid #e6e6e6;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            color: #333;
        }
        .avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: inline-block;
            vertical-align: middle;
            margin-right: 15px;
        }
    </style>
    """, unsafe_allow_html=True)



    # Message d'accueil
    first_txt = """Salut ! 👋 Je suis là pour transformer le dépannage en une tâche facile pour vous. Parlons de votre problème et découvrons les meilleures solutions ensemble."""
    sorry_text = """Je suis votre assistant de maintenance, et je peux répondre uniquement à des questions techniques liées à la maintenance industrielle."""



    # Organisation des chats par catégories (Aujourd'hui, Hier, Jours Précédents)
    def organize_chats():
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        chats_today = []
        chats_yesterday = []
        chats_previous = []

        for name in st.session_state.chat_history:
            if name.startswith(str(today)):
                chats_today.append(name)
            elif name.startswith(str(yesterday)):
                chats_yesterday.append(name)
            else:
                chats_previous.append(name)
        return chats_today, chats_yesterday, chats_previous



    # Fonction pour générer un nom de chat automatique
    def generate_chat_name():
        today = datetime.date.today()
        count = sum(1 for name in st.session_state.chat_history if name.startswith(str(today)))
        return f"{today} - Chat {count + 1}"


    # --- Fonction pour générer un titre de chat basé sur la première question ---
    def generate_chat_title(first_question):
        if len(first_question) > 30:
            return first_question[:27] + "..."  # Tronquer pour les titres longs
        return first_question

    # Sidebar avec les chats classés

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}

    st.sidebar.title("🗂️ Historique des Chats")




    # Bouton pour créer un nouveau chat
    if st.sidebar.button("➕ Nouveau Chat"):
        new_chat_name = generate_chat_name()
        st.session_state.chat_history[new_chat_name] = [{"role": "assistant", "message": "👋 Nouveau départ ! Posez-moi vos questions."}]
        st.session_state.messages = st.session_state.chat_history[new_chat_name]


    chats_today, chats_yesterday, chats_previous = organize_chats()
    # Affichage dans la sidebar
    if chats_today:
        st.sidebar.markdown("### 📅 Aujourd'hui")
        for chat in chats_today:
            if st.sidebar.button(chat):
                st.session_state.messages = st.session_state.chat_history[chat]

    if chats_yesterday:
        st.sidebar.markdown("### ⏳ Hier")
        for chat in chats_yesterday:
            if st.sidebar.button(chat):
                st.session_state.messages = st.session_state.chat_history[chat]

    if chats_previous:
        st.sidebar.markdown("### 📆 Jours précédents")
        for chat in chats_previous:
            if st.sidebar.button(chat):
                st.session_state.messages = st.session_state.chat_history[chat]




    # En-tête principal avec logo
    def local_image_to_base64(img_path):
        with open(img_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode('utf-8')

    img_base64 = local_image_to_base64("beeboy00.png")
    st.markdown(f"""
        <div style='text-align:center; margin-top:20px;'>
            <img src='data:image/png;base64,{img_base64}' 
                style='width:150px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);' />
        </div>
        <h1 style='text-align: center; color:#004080;'>BeeBoy - Votre Compagnon de Maintenance Industrielle</h1>
    """, unsafe_allow_html=True)



    # Fonction de complétion
    @st.cache_data
    def get_completion(user_input):
        # chat_prompt = [
        #     {"role": "system", "content": "Vous êtes un(e) assistant(e) IA expert(e) en maintenance industrielle."},
        #     {"role": "user", "content": user_input}
        # ]
        # completion = client.chat.completions.create(
        #     model=deployment,
        #     messages=chat_prompt,
        #     max_tokens=800,
        #     temperature=0.7
        # )
        # IMAGE_PATH = "YOUR_IMAGE_PATH"
        # encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

        #Préparer l’invite de conversation 
        # chat_prompt = [
        #     {
        #         "role": "system",
        #         "content": [
        #             {
        #                 "type": "text",
        #                 "text": "Je suis un assistant IA conçu pour aider les techniciens de maintenance dans leur diagnostic. J'ai accès aux données historiques des interventions de maintenance effectuées sur plusieurs machines du site. Lorsque vous rencontrez une panne, vous pouvez me poser une question, et je vous proposerai une solution en me basant sur les données passées et les interventions similaires déjà réalisées. Mon objectif est de vous faire gagner du temps et de simplifier le processus de diagnostic."
        #             }
        #         ]
        #     }
        # ] 

        chat_prompt = [
            {"role": "system", "content": "Je suis un assistant IA conçu pour aider les techniciens de maintenance dans leur diagnostic. J'ai accès aux données historiques des interventions de maintenance effectuées sur plusieurs machines du site. Lorsque vous rencontrez une panne, vous pouvez me poser une question, et je vous proposerai une solution en me basant sur les données passées et les interventions similaires déjà réalisées. Mon objectif est de vous faire gagner du temps et de simplifier le processus de diagnostic."},
            {"role": "user", "content": user_input}
        ]
            
        # Inclure le résultat de la voix si la voix est activée  
        messages = chat_prompt  
            
        # Générer l’achèvement  
        completion = client.chat.completions.create(  
            model=deployment,
            messages=messages,
            max_tokens=800,  
            temperature=0.7,  
            top_p=0.95,  
            frequency_penalty=0,  
            presence_penalty=0,
            stop=None,  
            stream=False,
            extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "endpoint": f"{search_endpoint}",
                    "index_name": "indexopenaibeeboy",
                    "semantic_configuration": "default",
                    "query_type": "semantic",
                    "fields_mapping": {},
                    "in_scope": True,
                    "role_information": "Je suis un assistant IA conçu pour aider les techniciens de maintenance dans leur diagnostic. J'ai accès aux données historiques des interventions de maintenance effectuées sur plusieurs machines du site. Lorsque vous rencontrez une panne, vous pouvez me poser une question, et je vous proposerai une solution en me basant sur les données passées et les interventions similaires déjà réalisées. Mon objectif est de vous faire gagner du temps et de simplifier le processus de diagnostic.",
                    "filter": None,
                    "strictness": 3,
                    "top_n_documents": 5,
                    "authentication": {
                    "type": "api_key",
                    "key": f"{search_key}"
                    }
                }
                }]
            }
        )

        return json.loads(completion.to_json())["choices"][0]["message"]["content"]

    # Chargement des commentaires
    df_commentaire = pd.read_excel("commentaire.xlsx")
    commentaire_liste = df_commentaire["Commentaire"].tolist()
    avis_liste = df_commentaire["Avis"].tolist()
    question_liste = df_commentaire["Question"].tolist()
    reponse_liste = df_commentaire["Réponse"].tolist()

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "message": first_txt}]

    # Entrée utilisateur
    user_input = st.chat_input("Posez votre question ici...")
    if user_input:
        response = get_completion(user_input)
        #st.toast("Vérification en cours...", icon="ℹ️")
        st.session_state.messages.append({"role": "user", "message": user_input})
        st.session_state.messages.append({"role": "assistant", "message": response})

    # Affichage des messages
    for idx, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            avatar = "🧑‍🔧"
            message_class = "user-message"
        else:
            avatar = "🧠"
            message_class = "assistant-message"

        st.markdown(f"""
        <div class='{message_class}'>
            <span class='avatar'>{avatar}</span>{message['message']}
        </div>
        """, unsafe_allow_html=True)

        # Ajouter un seul formulaire d'évaluation uniquement après les réponses de l'assistant
        if message["role"] == "assistant" and message["message"] != first_txt and idx == len(st.session_state.messages) - 1:
            with st.form(key=f"rating_form_{idx}"):
                st.markdown("### 📝 Évaluez la réponse")
                col1, col2 = st.columns(2)
                with col1:
                    commentaire = st.text_area("Votre commentaire :", placeholder="Donnez-nous votre avis ici...")
                with col2:
                    stars = st_star_rating("Notez la réponse", maxValue=5, defaultValue=1)
                submitted = st.form_submit_button("Envoyer")
                if submitted:
                    commentaire_liste.append(commentaire)
                    avis_liste.append(stars)
                    question_liste.append(st.session_state.messages[idx-1]["message"])
                    reponse_liste.append(message["message"])
                    pd.DataFrame({
                        'Question': question_liste,
                        'Réponse': reponse_liste,
                        'Commentaire': commentaire_liste,
                        'Avis': avis_liste
                    }).to_excel("commentaire.xlsx", index=False)
                    st.success("Merci pour votre retour ! 😊")


