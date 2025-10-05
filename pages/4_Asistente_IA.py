import streamlit as st
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from data.etapas import ETAPAS
from utils.asistente_ai import generar_respuesta_asistente, generar_plan_entrenamiento

st.set_page_config(
    page_title="Asistente IA",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Asistente Virtual de Entrenamiento")
st.markdown("Asistente personalizado con IA para ayudarte a preparar El Cruce Saucony 2025")

# Verificar API key
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "tu-api-key-aqui":
    st.error("⚠️ API Key de OpenAI no configurada")
    st.markdown("""
    Para usar el asistente con IA:
    
    1. Obtén tu API key en: https://platform.openai.com/api-keys
    2. Edita el archivo `.env` en la raíz del proyecto
    3. Reemplaza `OPENAI_API_KEY=tu-api-key-aqui` con tu key real
    4. Reinicia la aplicación
    """)
    st.stop()

st.divider()

# Tabs para diferentes funcionalidades
tab1, tab2 = st.tabs(["💬 Chat con el Asistente", "📋 Generar Plan de Entrenamiento"])

# TAB 1: Chat
with tab1:
    st.markdown("### Pregúntale cualquier cosa sobre El Cruce")
    
    # Inicializar historial de chat
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
    
    # Mostrar historial
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
    
    # Input del usuario
    if pregunta := st.chat_input("Escribe tu pregunta..."):
        # Agregar mensaje del usuario al historial
        st.session_state.mensajes.append({"role": "user", "content": pregunta})
        
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(pregunta)
        
        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                respuesta = generar_respuesta_asistente(
                    pregunta, 
                    ETAPAS,
                    st.session_state.mensajes[:-1]  # Historial sin el último mensaje
                )
                st.markdown(respuesta)
        
        # Agregar respuesta al historial
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
    
    # Botón para limpiar chat
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()
    
    # Ejemplos de preguntas
    with st.expander("💡 Ejemplos de preguntas"):
        st.markdown("""
        - ¿Cómo debo preparar la Etapa 1 que tiene tanto desnivel?
        - ¿Qué estrategia de hidratación me recomiendas para la Etapa 2?
        - Tengo 3 meses para entrenar, ¿por dónde empiezo?
        - ¿Cómo gestiono el pace en subidas pronunciadas?
        - ¿Qué debo comer en los oasis?
        - ¿Cuál etapa es más técnica y por qué?
        """)

# TAB 2: Plan de entrenamiento
with tab2:
    st.markdown("### Genera tu plan personalizado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        semanas = st.slider(
            "¿Cuántas semanas tienes hasta la carrera?",
            min_value=4,
            max_value=24,
            value=12,
            step=1
        )
        
        nivel = st.selectbox(
            "¿Cuál es tu nivel actual?",
            options=[
                "Principiante en trail (menos de 1 año)",
                "Intermedio (1-3 años de trail)",
                "Avanzado (más de 3 años de trail)"
            ]
        )
    
    with col2:
        pace_objetivo = st.slider(
            "¿Qué pace objetivo tienes? (min/km)",
            min_value=8.0,
            max_value=14.0,
            value=10.0,
            step=0.5
        )
        
        st.info(f"""
        Con {pace_objetivo} min/km completarías:
        - Etapa 1 (31km): ~{(31 * pace_objetivo / 60):.1f}h
        - Etapa 2 (32km): ~{(32 * pace_objetivo / 60):.1f}h
        - Etapa 3 (30km): ~{(30 * pace_objetivo / 60):.1f}h
        """)
    
    if st.button("🎯 Generar Plan de Entrenamiento", type="primary"):
        with st.spinner("Generando tu plan personalizado..."):
            plan = generar_plan_entrenamiento(semanas, nivel, pace_objetivo, ETAPAS)
            
            st.markdown("### Tu Plan de Entrenamiento")
            st.markdown(plan)
            
            st.download_button(
                label="📥 Descargar Plan (TXT)",
                data=plan,
                file_name=f"plan_entrenamiento_elcruce_{semanas}semanas.txt",
                mime="text/plain"
            )

st.divider()

# Información sobre costos
with st.expander("ℹ️ Sobre el uso de IA"):
    st.markdown("""
    **Este asistente usa GPT-4o-mini de OpenAI:**
    
    - Modelo: gpt-4o-mini (económico y eficiente)
    - Costo aproximado: $0.0001 - $0.0005 por respuesta
    - Tu crédito de $4 alcanza para ~8,000-40,000 consultas
    
    **Privacidad:**
    - Las conversaciones no se guardan en OpenAI
    - Se procesan en tiempo real y luego se descartan
    - Solo se almacenan en tu sesión local de Streamlit
    """)