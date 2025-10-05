import streamlit as st
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from data.etapas import ETAPAS, RESUMEN_EVENTO
from utils.visualizaciones import (
    grafico_comparativo_etapas,
    grafico_desnivel_por_km,
    grafico_altimetrias_superpuestas
)
from utils.calculadora import comparar_etapas, formato_tiempo, tiempo_limite_etapa

st.set_page_config(
    page_title="Comparativa de Etapas",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Comparativa de Etapas")
st.markdown("Compara las métricas y perfiles de las 3 etapas de El Cruce Saucony 2025")

st.divider()

# Métricas comparativas
col1, col2, col3 = st.columns(3)

comparacion = comparar_etapas(ETAPAS)

with col1:
    st.subheader("📏 Más Larga")
    etapa_larga = comparacion["mas_larga"]
    st.info(f"**{etapa_larga['nombre']}**")
    st.metric("Distancia", f"{etapa_larga['distancia_km']} km")

with col2:
    st.subheader("⛰️ Más Desnivel")
    etapa_desnivel = comparacion["mas_desnivel"]
    st.info(f"**{etapa_desnivel['nombre']}**")
    st.metric("Desnivel +", f"{etapa_desnivel['desnivel_positivo']} m")

with col3:
    st.subheader("📈 Más Intensa")
    etapa_intensa = comparacion["mas_desnivel_por_km"]
    st.info(f"**{etapa_intensa['nombre']}**")
    desnivel_km = etapa_intensa['desnivel_positivo'] / etapa_intensa['distancia_km']
    st.metric("Intensidad", f"{desnivel_km:.1f} m/km")

st.divider()

# Tabla comparativa
st.subheader("📊 Tabla Comparativa")

import pandas as pd

datos_tabla = []
for etapa in ETAPAS:
    tiempo_lim = tiempo_limite_etapa(etapa['distancia_km'])
    datos_tabla.append({
        "Etapa": etapa['nombre'],
        "Distancia (km)": etapa['distancia_km'],
        "Desnivel + (m)": etapa['desnivel_positivo'],
        "Intensidad (m/km)": f"{etapa['desnivel_positivo']/etapa['distancia_km']:.1f}",
        "Tiempo Límite": formato_tiempo(tiempo_lim),
        "Oasis": len(etapa['oasis'])
    })

df = pd.DataFrame(datos_tabla)
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# Gráficos comparativos
st.subheader("📊 Comparación Visual")

tab1, tab2, tab3 = st.tabs(["Distancia y Desnivel", "Intensidad", "Perfiles Superpuestos"])

with tab1:
    fig1 = grafico_comparativo_etapas(ETAPAS)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = grafico_desnivel_por_km(ETAPAS)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = grafico_altimetrias_superpuestas(ETAPAS)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Análisis estratégico
st.subheader("💡 Análisis Estratégico")

col_analisis1, col_analisis2 = st.columns(2)

with col_analisis1:
    st.markdown("#### Distribución del esfuerzo")
    total_desnivel = sum(e['desnivel_positivo'] for e in ETAPAS)
    
    for etapa in ETAPAS:
        porcentaje = (etapa['desnivel_positivo'] / total_desnivel) * 100
        st.markdown(f"**{etapa['nombre']}:** {porcentaje:.1f}% del desnivel total")

with col_analisis2:
    st.markdown("#### Recomendaciones")
    st.markdown("""
    - **Etapa 1:** La más técnica, gestiona bien el ritmo inicial
    - **Etapa 2:** Recuperación activa, mantén ritmo constante
    - **Etapa 3:** Gran ascenso, reserva energía para el final
    """)

st.divider()

# Calculadora de tiempos acumulados
with st.expander("🧮 Simular tiempos acumulados"):
    st.markdown("Calcula el tiempo total estimado según tu pace promedio")
    
    pace_simulacion = st.slider(
        "Pace promedio estimado (min/km):",
        min_value=6.0,
        max_value=15.0,
        value=10.0,
        step=0.5
    )
    
    tiempo_total = 0
    for etapa in ETAPAS:
        tiempo_etapa = (etapa['distancia_km'] * pace_simulacion) / 60
        tiempo_total += tiempo_etapa
        tiempo_limite = tiempo_limite_etapa(etapa['distancia_km'])
        
        col_sim1, col_sim2, col_sim3 = st.columns(3)
        with col_sim1:
            st.metric(etapa['nombre'], etapa['distancia_km'])
        with col_sim2:
            st.metric("Tiempo estimado", formato_tiempo(tiempo_etapa))
        with col_sim3:
            if tiempo_etapa <= tiempo_limite:
                st.success("✅ Dentro del límite")
            else:
                st.error("⚠️ Excede límite")
    
    st.divider()
    st.info(f"**Tiempo total estimado:** {formato_tiempo(tiempo_total)}")