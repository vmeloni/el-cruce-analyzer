"""
Funciones de visualización con Plotly para El Cruce Analyzer
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def grafico_altimetria(etapa, mostrar_oasis=True):
    """
    Crea gráfico de altimetría para una etapa.
    
    Args:
        etapa: Dict con datos de la etapa
        mostrar_oasis: Bool para mostrar ubicación de oasis
    
    Returns:
        Figura de Plotly
    """
    # Extraer datos del perfil
    distancias = [punto[0] for punto in etapa["perfil"]]
    altitudes = [punto[1] for punto in etapa["perfil"]]
    
    # Crear figura
    fig = go.Figure()
    
    # Agregar perfil de altimetría (área rellena)
    fig.add_trace(go.Scatter(
        x=distancias,
        y=altitudes,
        mode='lines',
        name='Altitud',
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.3)',
        line=dict(color='rgb(31, 119, 180)', width=3),
        hovertemplate='<b>Km %{x:.1f}</b><br>Altitud: %{y}m<extra></extra>'
    ))
    
    # Agregar marcadores de oasis si está habilitado
    if mostrar_oasis and etapa.get("oasis"):
        for oasis in etapa["oasis"]:
            km_oasis = oasis["km"]
            # Interpolar altitud en la posición del oasis
            altitud_oasis = interpolar_altitud(etapa["perfil"], km_oasis)
            
            fig.add_trace(go.Scatter(
                x=[km_oasis],
                y=[altitud_oasis],
                mode='markers+text',
                name=oasis["nombre"],
                marker=dict(size=12, color='red', symbol='circle'),
                text=[f"💧 {oasis['nombre']}"],
                textposition="top center",
                textfont=dict(size=10),
                hovertemplate=f'<b>{oasis["nombre"]}</b><br>Km {km_oasis}<extra></extra>'
            ))
    
    # Configurar layout
    fig.update_layout(
        title=f"{etapa['nombre']} - Perfil de Altimetría",
        xaxis_title="Distancia (km)",
        yaxis_title="Altitud (m)",
        hovermode='x unified',
        showlegend=False,
        height=400,
        template="plotly_white",
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Configurar ejes
    fig.update_xaxes(range=[0, etapa["distancia_km"]], gridcolor='lightgray')
    fig.update_yaxes(gridcolor='lightgray')
    
    return fig


def interpolar_altitud(perfil, km_objetivo):
    """
    Interpola la altitud en un kilómetro específico del perfil.
    
    Args:
        perfil: Lista de tuplas (km, altitud)
        km_objetivo: Kilómetro donde calcular altitud
    
    Returns:
        Altitud interpolada (float)
    """
    # Encontrar los dos puntos más cercanos
    for i in range(len(perfil) - 1):
        km1, alt1 = perfil[i]
        km2, alt2 = perfil[i + 1]
        
        if km1 <= km_objetivo <= km2:
            # Interpolación lineal
            proporcion = (km_objetivo - km1) / (km2 - km1)
            return alt1 + proporcion * (alt2 - alt1)
    
    # Si está fuera de rango, devolver el más cercano
    return perfil[-1][1]


def grafico_comparativo_etapas(etapas):
    """
    Crea gráfico comparativo de métricas entre etapas.
    
    Args:
        etapas: Lista de dicts con datos de etapas
    
    Returns:
        Figura de Plotly
    """
    nombres = [e["nombre"] for e in etapas]
    distancias = [e["distancia_km"] for e in etapas]
    desniveles = [e["desnivel_positivo"] for e in etapas]
    
    # Crear subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Distancia (km)', 'Desnivel Positivo (m)'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Gráfico de distancias
    fig.add_trace(
        go.Bar(
            x=nombres,
            y=distancias,
            name="Distancia",
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
            text=distancias,
            texttemplate='%{text} km',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>%{y} km<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Gráfico de desniveles
    fig.add_trace(
        go.Bar(
            x=nombres,
            y=desniveles,
            name="Desnivel",
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
            text=desniveles,
            texttemplate='%{text}m',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>%{y}m<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Layout
    fig.update_layout(
        showlegend=False,
        height=400,
        template="plotly_white",
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_yaxes(title_text="Kilómetros", row=1, col=1)
    fig.update_yaxes(title_text="Metros", row=1, col=2)
    
    return fig


def grafico_desnivel_por_km(etapas):
    """
    Gráfico de desnivel por kilómetro (intensidad) de cada etapa.
    
    Args:
        etapas: Lista de dicts con datos de etapas
    
    Returns:
        Figura de Plotly
    """
    nombres = [e["nombre"] for e in etapas]
    desnivel_km = [e["desnivel_positivo"] / e["distancia_km"] for e in etapas]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=nombres,
        y=desnivel_km,
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
        text=[f"{d:.1f} m/km" for d in desnivel_km],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>%{y:.1f} m/km<extra></extra>'
    ))
    
    fig.update_layout(
        title="Intensidad: Desnivel por Kilómetro",
        xaxis_title="Etapa",
        yaxis_title="Desnivel por km (m/km)",
        height=400,
        template="plotly_white",
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig


def grafico_altimetrias_superpuestas(etapas):
    """
    Superpone los perfiles de altimetría de todas las etapas.
    
    Args:
        etapas: Lista de dicts con datos de etapas
    
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    
    colores = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, etapa in enumerate(etapas):
        distancias = [punto[0] for punto in etapa["perfil"]]
        altitudes = [punto[1] for punto in etapa["perfil"]]
        
        fig.add_trace(go.Scatter(
            x=distancias,
            y=altitudes,
            mode='lines',
            name=etapa["nombre"],
            line=dict(color=colores[i], width=3),
            hovertemplate='<b>' + etapa["nombre"] + '</b><br>Km %{x:.1f}<br>Alt: %{y}m<extra></extra>'
        ))
    
    fig.update_layout(
        title="Comparación de Perfiles de Altimetría",
        xaxis_title="Distancia (km)",
        yaxis_title="Altitud (m)",
        hovermode='x unified',
        height=500,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=50, t=100, b=50)
    )
    
    return fig