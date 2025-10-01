import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Talk to Steve 🇫🇷",
    page_icon="🇫🇷",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1E3A8A;
        padding: 20px 0;
    }
    .steve-container {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin: 20px 0;
    }
    .steve-image {
        font-size: 100px;
        margin: 20px 0;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: #1E293B !important;
        font-weight: 500;
    }
    .chat-message strong {
        color: #0F172A;
    }
    .user-message {
        background-color: #E0E7FF;
        text-align: right;
        color: #1E293B;
    }
    .steve-message {
        background-color: #F3F4F6;
        text-align: left;
        color: #1E293B;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # System prompt - Steve's personality
    st.session_state.system_prompt = {
        "role": "system",
        "content": """Tu es Steve, un collègue français qui travaille dans une entreprise tech. 
        Tu es décontracté mais professionnel. Tu aimes parler de:
        - Projets de travail et collaboration
        - Technologie et innovation
        - Pauses café et vie au bureau
        - Plans pour le weekend
        
        IMPORTANT:
        - Garde tes réponses courtes (2-3 phrases maximum)
        - Utilise un français moderne et casual
        - Pose des questions pour maintenir la conversation
        - Sois amical et encourageant
        - Corrige gentiment les erreurs sans être condescendant
        
        Exemple de ton style:
        "Salut! Ça va bien aujourd'hui? Tu bosses sur quoi en ce moment?"
        """
    }

# Header with logo
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("AI_LOGO.webp", use_container_width=True)
    
st.markdown("<h1 class='main-header'>🇫🇷 Parle avec Steve</h1>", unsafe_allow_html=True)

# Steve's character display
st.markdown("""
    <div class='steve-container'>
        <div class='steve-image'>👨‍💼</div>
        <h2 style='color: white; margin: 0;'>Steve</h2>
        <p style='color: white; margin: 5px 0;'>Ton collègue français</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ À propos")
    st.write("**Steve** est ton collègue français dans une entreprise tech.")
    st.write("Pratique ton français en parlant avec lui!")
    
    st.divider()
    
    st.subheader("💡 Sujets de conversation:")
    st.write("- Projets de travail")
    st.write("- Technologie")
    st.write("- Pause café")
    st.write("- Plans weekend")
    
    st.divider()
    
    if st.button("🔄 Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("💬 Version texte MVP")
    st.caption("⚡ Powered by Groq")

# Display conversation history
if st.session_state.messages:
    st.subheader("💬 Conversation")
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class='chat-message user-message'>
                    <strong>Toi:</strong> {message['content']}
                </div>
            """, unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f"""
                <div class='chat-message steve-message'>
                    <strong>Steve:</strong> {message['content']}
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("👋 Dis bonjour à Steve pour commencer la conversation!")

# User input
st.divider()

# Use a dynamic key that changes after each message to clear the input
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

user_input = st.text_input(
    "Écris ton message en français:",
    placeholder="Ex: Bonjour Steve, comment ça va?",
    key=f"user_input_{st.session_state.input_key}"
)

col1, col2 = st.columns([3, 1])
with col1:
    send_button = st.button("📤 Envoyer", use_container_width=True, type="primary")

# Process message when button is clicked
if send_button and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Show loading state
    with st.spinner("Steve réfléchit..."):
        try:
            # Prepare messages for API (include system prompt)
            api_messages = [st.session_state.system_prompt] + st.session_state.messages
            
            # Call Groq API
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Fast and good model
                messages=api_messages,
                temperature=0.8,  # More creative/casual
                max_tokens=150  # Keep responses short
            )
            
            # Get Steve's response
            steve_response = response.choices[0].message.content
            
            # Add to conversation history
            st.session_state.messages.append({
                "role": "assistant",
                "content": steve_response
            })
            
            # Increment input key to clear the text field
            st.session_state.input_key += 1
            
            # Rerun to show updated conversation
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
            st.info("Vérifie que ta clé API Groq est correcte dans le fichier .env")

# Footer
st.divider()
st.caption("🚀 Fait avec Streamlit + Groq | 🇫🇷 Apprends le français avec Steve")
