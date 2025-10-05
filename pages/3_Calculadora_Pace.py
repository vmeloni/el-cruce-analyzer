import streamlit as st
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from data.etapas import ETAPAS, RESUMEN_EVENTO
from utils.calculadora import (
    calcular_tiempo_estimado,
    calcular_pace_necesario,
    tiempo_limite_etapa,
    estimar_calorias,
    formato_tiempo
)

st.set_page_config(
    page_title="Calculadora de Pace",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Calculadora de Pace y Estrategia")
st.markdown("Calcula tiempos, pace y estrategia para completar El Cruce")

st.divider()

# Selector de modo
modo = st.radio(
    "¿Qué quieres calcular?",
    options=["Tiempo según mi pace", "Pace necesario para un tiempo objetivo"],
    horizontal=True
)

st.divider()

if modo == "Tiempo según mi pace":
    st.subheader("⏱️ Calcular tiempo estimado según tu pace")
    
    col_input, col_output = st.columns([1, 2])
    
    with col_input:
        st.markdown("#### Parámetros")
        
        pace_promedio = st.number_input(
            "Tu pace promedio (min/km):",
            min_value=6.0,
            max_value=15.0,
            value=10.0,
            step=0.5,
            help="Pace estimado considerando terreno montañoso"
        )
        
        peso = st.number_input(
            "Tu peso (kg):",
            min_value=40,
            max_value=120,
            value=70,
            step=1
        )
    
    with col_output:
        st.markdown("#### Resultados por etapa")
        
        tiempo_total_carrera = 0
        calorias_totales = 0
        
        for i, etapa in enumerate(ETAPAS):
            with st.container():
                st.markdown(f"**{etapa['nombre']}** - {etapa['distancia_km']}km")
                
                tiempo_estimado = calcular_tiempo_estimado(etapa['distancia_km'], pace_promedio)
                tiempo_limite = tiempo_limite_etapa(etapa['distancia_km'])
                calorias = estimar_calorias(etapa['distancia_km'], etapa['desnivel_positivo'], peso)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Tiempo estimado", formato_tiempo(tiempo_estimado))
                
                with col2:
                    st.metric("Tiempo límite", formato_tiempo(tiempo_limite))
                
                with col3:
                    st.metric("Calorías", f"{calorias:,}")
                
                # Indicador de cumplimiento
                if tiempo_estimado <= tiempo_limite:
                    margen = tiempo_limite - tiempo_estimado
                    st.success(f"✅ Cumplirías con {formato_tiempo(margen)} de margen")
                else:
                    exceso = tiempo_estimado - tiempo_limite
                    st.error(f"⚠️ Te faltarían {formato_tiempo(exceso)}")
                
                tiempo_total_carrera += tiempo_estimado
                calorias_totales += calorias
                
                if i < len(ETAPAS) - 1:
                    st.divider()
        
        st.divider()
        
        # Totales
        st.markdown("#### Totales de la carrera")
        col_tot1, col_tot2 = st.columns(2)
        
        with col_tot1:
            st.metric("Tiempo total estimado", formato_tiempo(tiempo_total_carrera))
        
        with col_tot2:
            st.metric("Calorías totales", f"{calorias_totales:,}")

else:  # Pace necesario para un tiempo objetivo
    st.subheader("🎯 Calcular pace necesario para un tiempo objetivo")
    
    etapa_objetivo = st.selectbox(
        "Selecciona la etapa:",
        options=[0, 1, 2],
        format_func=lambda x: f"{ETAPAS[x]['nombre']}: {ETAPAS[x]['distancia_km']}km"
    )
    
    etapa = ETAPAS[etapa_objetivo]
    
    col_obj1, col_obj2 = st.columns(2)
    
    with col_obj1:
        st.markdown("#### Objetivo")
        
        horas = st.number_input(
            "Horas:",
            min_value=0,
            max_value=12,
            value=5,
            step=1
        )
        
        minutos = st.number_input(
            "Minutos:",
            min_value=0,
            max_value=59,
            value=0,
            step=5
        )
        
        tiempo_objetivo = horas + (minutos / 60)
        
        st.info(f"Objetivo: **{formato_tiempo(tiempo_objetivo)}**")
    
    with col_obj2:
        st.markdown("#### Pace necesario")
        
        pace_necesario = calcular_pace_necesario(etapa['distancia_km'], tiempo_objetivo)
        tiempo_limite = tiempo_limite_etapa(etapa['distancia_km'])
        pace_limite = 15.0  # min/km
        
        st.metric("Pace requerido", f"{pace_necesario:.2f} min/km")
        
        if pace_necesario <= pace_limite:
            st.success(f"✅ Pace dentro del límite ({pace_limite} min/km)")
        else:
            st.error(f"⚠️ Pace excede el límite de {pace_limite} min/km")
        
        # Comparación con tiempo límite
        if tiempo_objetivo <= tiempo_limite:
            margen = tiempo_limite - tiempo_objetivo
            st.success(f"Tendrías {formato_tiempo(margen)} de margen")
        else:
            st.error("⚠️ El objetivo excede el tiempo límite")

st.divider()

# Recomendaciones de estrategia
with st.expander("💡 Recomendaciones de estrategia de pace"):
    st.markdown("""
    ### Gestión del Pace en Trail Running de Montaña
    
    **Ajusta tu pace según el terreno:**
    
    - **Subidas pronunciadas (>10%):** Camina a paso firme (12-15 min/km o más)
    - **Subidas moderadas (5-10%):** Trote lento (10-12 min/km)
    - **Terreno plano:** Tu pace habitual (8-10 min/km)
    - **Bajadas moderadas:** Pace controlado (7-9 min/km)
    - **Bajadas técnicas:** Pace conservador para evitar lesiones (9-11 min/km)
    
    **Distribución del esfuerzo:**
    
    1. **Etapa 1:** Salida conservadora. El ascenso inicial es exigente.
    2. **Etapa 2:** Mantén ritmo constante, gestiona las ondulaciones.
    3. **Etapa 3:** Dosifica en el ascenso largo, aprovecha el descenso final.
    
    **Factores a considerar:**
    
    - Altitud (menor rendimiento sobre 1500m)
    - Clima patagónico (viento, frío, lluvia)
    - Acumulación de fatiga entre etapas
    - Superficie técnica (piedras, raíces, barro)
    - Tu experiencia en montaña
    """)

st.divider()

# Planificador de oasis
with st.expander("🥤 Planificador de hidratación y alimentación"):
    st.markdown("### Estrategia de Oasis")
    
    etapa_plan = st.selectbox(
        "Selecciona etapa para planificar:",
        options=[0, 1, 2],
        format_func=lambda x: ETAPAS[x]['nombre'],
        key="plan_etapa"
    )
    
    etapa_sel = ETAPAS[etapa_plan]
    pace_plan = st.slider(
        "Tu pace estimado (min/km):",
        6.0, 15.0, 10.0, 0.5,
        key="pace_plan"
    )
    
    st.markdown(f"#### {etapa_sel['nombre']}")
    
    tiempo_transcurrido = 0
    
    for i, oasis in enumerate(etapa_sel['oasis']):
        km_oasis = oasis['km']
        
        if i == 0:
            distancia_tramo = km_oasis
        else:
            distancia_tramo = km_oasis - etapa_sel['oasis'][i-1]['km']
        
        tiempo_tramo = calcular_tiempo_estimado(distancia_tramo, pace_plan)
        tiempo_transcurrido += tiempo_tramo
        
        st.markdown(f"**{oasis['nombre']}** (km {km_oasis})")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"Llegarás aproximadamente a las {formato_tiempo(tiempo_transcurrido)} de carrera")
        
        with col2:
            st.markdown("**Recomendación:**")
            st.markdown("- 200-300ml de líquido")
            st.markdown("- 1 gel o snack energético")
            if km_oasis > 15:
                st.markdown("- Comida sólida (fruta, barras)")

st.divider()

st.caption("⚡ Los cálculos son estimaciones. Ajústalos según tu experiencia y condiciones del día.")