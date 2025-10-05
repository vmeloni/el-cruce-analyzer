import streamlit as st
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from data.etapas import ETAPAS, RESUMEN_EVENTO
from utils.visualizaciones import grafico_altimetria
from utils.calculadora import (
    calcular_desnivel_por_km,
    tiempo_limite_etapa,
    estimar_calorias,
    formato_tiempo
)

# Configuración de la página
st.set_page_config(
    page_title="Análisis por Etapa",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Análisis por Etapa")
st.markdown("Análisis detallado de cada etapa de El Cruce Saucony 2025")

st.divider()

# Selector de etapa
etapa_seleccionada = st.selectbox(
    "Selecciona una etapa:",
    options=[0, 1, 2],
    format_func=lambda x: f"Etapa {x+1}: {ETAPAS[x]['distancia_km']}km | +{ETAPAS[x]['desnivel_positivo']}m",
    index=0
)

etapa = ETAPAS[etapa_seleccionada]

st.divider()

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📏 Distancia", f"{etapa['distancia_km']} km")

with col2:
    st.metric("⛰️ Desnivel +", f"{etapa['desnivel_positivo']} m")

with col3:
    desnivel_km = calcular_desnivel_por_km(
        etapa['desnivel_positivo'], 
        etapa['distancia_km']
    )
    st.metric("📈 Intensidad", f"{desnivel_km:.1f} m/km")

with col4:
    tiempo_lim = tiempo_limite_etapa(etapa['distancia_km'])
    st.metric("⏱️ Tiempo Límite", formato_tiempo(tiempo_lim))

st.divider()

# Información detallada
col_info, col_oasis = st.columns([2, 1])

with col_info:
    st.subheader("ℹ️ Información")
    st.markdown(f"""
    - **Inicio:** {etapa['inicio']}
    - **Fin:** {etapa['fin']}
    - **Características:** {etapa['caracteristicas']}
    """)

with col_oasis:
    st.subheader("💧 Oasis de Hidratación")
    for oasis in etapa['oasis']:
        st.markdown(f"- **{oasis['nombre']}** (km {oasis['km']})")

st.divider()

# Gráfico de altimetría
st.subheader("📈 Perfil de Altimetría")

mostrar_oasis = st.checkbox("Mostrar ubicación de oasis", value=True)

fig = grafico_altimetria(etapa, mostrar_oasis=mostrar_oasis)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Calculadora rápida
st.subheader("🧮 Estimaciones")

col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    st.markdown("**Tiempo estimado según tu pace:**")
    pace_usuario = st.slider(
        "Tu pace estimado (min/km):",
        min_value=6.0,
        max_value=15.0,
        value=10.0,
        step=0.5,
        key=f"pace_etapa_{etapa_seleccionada}"
    )
    
    tiempo_estimado = (etapa['distancia_km'] * pace_usuario) / 60
    st.info(f"⏱️ Tiempo estimado: **{formato_tiempo(tiempo_estimado)}**")
    
    # Verificar si cumple tiempo límite
    if tiempo_estimado <= tiempo_lim:
        st.success("✅ Cumplirías el tiempo límite")
    else:
        st.error("⚠️ Excederías el tiempo límite")

with col_calc2:
    st.markdown("**Gasto calórico estimado:**")
    peso_usuario = st.number_input(
        "Tu peso (kg):",
        min_value=40,
        max_value=120,
        value=70,
        step=1,
        key=f"peso_etapa_{etapa_seleccionada}"
    )
    
    calorias = estimar_calorias(
        etapa['distancia_km'],
        etapa['desnivel_positivo'],
        peso_usuario
    )
    st.info(f"🔥 Calorías estimadas: **~{calorias:,} kcal**")

st.divider()

# Tips
with st.expander("💡 Consejos para esta etapa"):
    if etapa_seleccionada == 0:
        st.markdown("""
        **Etapa 1 - La más técnica:**
        - Gestiona bien el ascenso inicial hasta los 1800m
        - Mantén un ritmo conservador en los primeros 10km
        - Hidratación clave en el Oasis B (km 16)
        - Cuida las rodillas en los descensos después del km 12
        """)
    elif etapa_seleccionada == 1:
        st.markdown("""
        **Etapa 2 - La ondulada:**
        - Múltiples subidas y bajadas, dosifica tu energía
        - Ritmo constante, evita arranques en cada subida
        - Descansa bien en el Campamento 1 la noche anterior
        - Alimentación sólida importante en los oasis
        """)
    else:
        st.markdown("""
        **Etapa 3 - El gran ascenso:**
        - Primera mitad muy exigente (ascenso continuo hasta km 16)
        - Aprovecha el descenso final para recuperar tiempo
        - Control en las bajadas para evitar lesiones
        - ¡Es la última etapa, da todo pero inteligentemente!
        """)