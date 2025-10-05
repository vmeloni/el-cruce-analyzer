import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="El Cruce Analyzer",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🏔️ El Cruce Saucony 2025 - Analyzer")
st.markdown("### Villa La Angostura | 1-7 Diciembre 2025")

st.divider()

# Información del evento
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📏 Distancia Total", "~93 km")
    st.metric("📅 Etapas", "3 días")

with col2:
    st.metric("⛰️ Desnivel Total", "+4,400m")
    st.metric("🏕️ Campamentos", "2")

with col3:
    st.metric("⏱️ Tiempo Límite", "15 min/km")
    st.metric("💧 Oasis", "7 puntos")

st.divider()

# Resumen de etapas
st.subheader("📊 Resumen de Etapas")

etapa1, etapa2, etapa3 = st.columns(3)

with etapa1:
    st.markdown("#### Etapa 1")
    st.info("**31K | +1,600m**")
    st.markdown("- Inicio: Olas\n- Fin: Camp 1\n- 3 Oasis")

with etapa2:
    st.markdown("#### Etapa 2")
    st.info("**32K | +1,300m**")
    st.markdown("- Inicio: Camp 1\n- Fin: Camp 2\n- 2 Oasis")

with etapa3:
    st.markdown("#### Etapa 3")
    st.info("**30K | +1,500m**")
    st.markdown("- Inicio: Camp 2\n- Fin: Villa La Angostura\n- 2 Oasis")

st.divider()

# Instrucciones
st.subheader("🧭 Cómo usar este dashboard")

st.markdown("""
Usa el menú del sidebar para navegar entre las diferentes secciones:

- **📊 Análisis Etapas:** Perfil de altimetría y detalles de cada etapa
- **📈 Comparativa:** Compara las 3 etapas (próximamente)
- **⚡ Calculadora de Pace:** Calcula tiempos y estrategia (próximamente)
- **🤖 Asistente IA:** Asistente personalizado con OpenAI (próximamente)
""")

st.divider()

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ Sobre el proyecto")
    st.markdown("""
    Dashboard interactivo para analizar las etapas de **El Cruce Saucony 2025**.
    
    Incluye análisis de altimetría, cálculos de pace, estrategia y asistente con IA.
    """)
    
    st.markdown("---")
    st.caption("🏔️ Datos oficiales de altimetría | Desarrollado con Streamlit")