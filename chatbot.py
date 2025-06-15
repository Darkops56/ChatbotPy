import streamlit as st
import groq

modelos = ["llama3-70b-8192", "llama3-8b-8192", "gemma-7b-it"]

print(groq.__version__)

def configurar_pagina():
    st.set_page_config(
        page_title="chatbot")
    st.title("Bienvenido a mi chatbot")
def crear_cliente():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key = groq_api_key)
def mostrar_sidebar():
    st.sidebar.title("elige un modelo")
    modelo = st.sidebar.selectbox("Selecciona un modelo", modelos, index=0)
    st.write(f"Modelo seleccionado: {modelo}")
    return modelo
def mensaje_usuario():
    return st.chat_input("Escribe tu mensaje.")
def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
def agregar_mensaje_previos(role, content):
    st.session_state.mensajes.append({
        "role": role,
        "content": content
    })
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)
def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta = cliente.chat.completions.create(
        model = modelo,
        messages=[{"role": "user", "content": mensaje}],
        stream=False,
    )
    return respuesta.choices[0].message.content
    
def ejecutar_chatbot():
    configurar_pagina()
    inicializar_estado_chat()
    cliente = crear_cliente()
    modelo = mostrar_sidebar()
    mensaje = mensaje_usuario()
    obtener_mensajes_previos()
    if mensaje:
        agregar_mensaje_previos("user", mensaje)
        mostrar_mensaje("user", mensaje)

        respuesta = obtener_respuesta_modelo(cliente, modelo, mensaje)

        agregar_mensaje_previos("assistant", respuesta)
        mostrar_mensaje("assistant", respuesta)

if __name__ == "__main__":
    ejecutar_chatbot()


