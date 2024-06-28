# Importando as Bibliotecas
import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv
import csv

# Configurando API Key
load_dotenv() 
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Selecionando o modelo
model_name = 'gemini-1.5-flash'
safety_settings = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

system_instruction = { """
    Você é RayAssist, um amigável assistente que ajuda os colaboradores da Raymundo da Fonte a buscar informações e análises de dados 
    sobre customer service da empresa.
    Não responda nenhuma resposta até o usuário dar passar nome e email. 
    Se o email não tiver @rfonte.com.br encerre o chat.
    """
  }

model = genai.GenerativeModel(
  model_name = model_name,
  safety_settings = safety_settings,
  generation_config = generation_config,
  #tools = ,
  #tool_config = ,
  system_instruction = system_instruction,
  )

# Selecionando os Dados
def extract_csv(pathname: str) -> list[str]:
    parts = [f"--- LENDO CSV $ {pathname} ---"]
    with open(pathname, "r", newline="") as csvfile:
        csv_reader=csv.reader(csvfile)
        for row in csv_reader:
            str=" "
            parts.append(str.join(row))
    return parts

# Chatbot
st.set_page_config(
    page_title="RayAssist",
    page_icon="🤖",
    layout="centered",
    )

st.title("RayAssist")
st.subheader ("A sua agente de IA para Customer Service da Raymundo da Fonte")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[
        {"role": "user",
         "parts": extract_csv("base_pedidos.csv")}
    ])

# Roles
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Initialize chat history
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("Em que posso ajudar?"):
    st.chat_message("user").markdown(prompt)
    response = st.session_state.chat.send_message(prompt)
    with st.chat_message('assistant'):
        st.markdown(response.text)









############# Execução do Código #################
# executar no terminal: streamlit run app.py