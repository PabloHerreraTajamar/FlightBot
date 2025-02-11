import streamlit as st
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

# Cargar variables de entorno
load_dotenv()
ls_prediction_endpoint = os.getenv('LS_CONVERSATIONS_ENDPOINT')
ls_prediction_key = os.getenv('LS_CONVERSATIONS_KEY')

# Configurar cliente de Azure
client = ConversationAnalysisClient(
    ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key)
)

# Configuración del proyecto en Azure
cls_project = 'FlightBot'
deployment_slot = 'FlightBot'

# Interfaz de usuario con Streamlit
st.title("Chatbot de Vuelos ✈️")
st.write("Escribe una consulta sobre vuelos y el bot identificará la intención y las entidades.")

# Sugerencias de preguntas
test_questions = [
    "¿Cuáles son los vuelos disponibles de Madrid a Nueva York?",
    "Quiero cambiar la fecha de mi vuelo",
    "¿Cuánto equipaje puedo llevar en el vuelo de Barcelona a Roma?",
    "¿A qué hora sale mi vuelo?"
]

st.subheader("💡 Preguntas sugeridas:")
cols = st.columns(4)
userText = ""

button_styles = """
    <style>
        .stButton>button {
            height: 100px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 16px;
            border-radius: 8px;
        }
    </style>
"""
st.markdown(button_styles, unsafe_allow_html=True)

for i, question in enumerate(test_questions):
    with cols[i]:
        if st.button(question, use_container_width=True, key=f"btn_{i}"):
            userText = question

st.write("**Introduce tu consulta:**")

col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    userText = st.text_input(
        "Consulta del usuario",
        value=userText,
        label_visibility="collapsed"
    )

with col2:
    if st.button("✉️", help="Enviar"):
        pass

with col3:
    if st.button("🗑️", help="Borrar"):
        userText = ""

if userText:
    with client:
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": userText
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": cls_project,
                    "deploymentName": deployment_slot,
                    "verbose": True
                }
            }
        )
    
    # Obtener intención principal
    top_intent = result["result"]["prediction"]["topIntent"]
    confidence_score = result["result"]["prediction"]["intents"][0]["confidenceScore"]
    entities = result["result"]["prediction"]["entities"]
    
    # Mostrar resultados
    st.subheader("🔍 Resultado de la predicción")
    st.write(f"**Intención detectada:** {top_intent}")
    
    # Mostrar entidades detectadas
    if entities:
        st.subheader("📌 Entidades detectadas")
        for entity in entities:
            st.write(f"- **Categoría:** {entity['category']}")
            st.write(f"  **Texto:** {entity['text']}")
    else:
        st.write("No se detectaron entidades.")