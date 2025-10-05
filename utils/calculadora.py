"""
Funciones de cálculo para El Cruce Analyzer
"""

def calcular_tiempo_estimado(distancia_km, pace_min_km):
    """
    Calcula el tiempo estimado para completar una distancia dado un pace.
    
    Args:
        distancia_km: Distancia en kilómetros
        pace_min_km: Pace en minutos por kilómetro
    
    Returns:
        Tiempo en horas (float)
    """
    tiempo_minutos = distancia_km * pace_min_km
    return tiempo_minutos / 60


def calcular_pace_necesario(distancia_km, tiempo_objetivo_horas):
    """
    Calcula el pace necesario para completar una distancia en un tiempo objetivo.
    
    Args:
        distancia_km: Distancia en kilómetros
        tiempo_objetivo_horas: Tiempo objetivo en horas
    
    Returns:
        Pace en minutos por kilómetro (float)
    """
    tiempo_minutos = tiempo_objetivo_horas * 60
    return tiempo_minutos / distancia_km


def tiempo_limite_etapa(distancia_km, tiempo_limite_min_km=15):
    """
    Calcula el tiempo límite para completar una etapa.
    
    Args:
        distancia_km: Distancia de la etapa en km
        tiempo_limite_min_km: Tiempo límite en min/km (default: 15)
    
    Returns:
        Tiempo límite en horas (float)
    """
    return calcular_tiempo_estimado(distancia_km, tiempo_limite_min_km)


def calcular_desnivel_por_km(desnivel_m, distancia_km):
    """
    Calcula el desnivel promedio por kilómetro.
    
    Args:
        desnivel_m: Desnivel positivo en metros
        distancia_km: Distancia en kilómetros
    
    Returns:
        Desnivel por km en metros (float)
    """
    return desnivel_m / distancia_km


def estimar_calorias(distancia_km, desnivel_m, peso_kg=70):
    """
    Estima las calorías quemadas en trail running.
    Fórmula aproximada considerando terreno montañoso.
    
    Args:
        distancia_km: Distancia en kilómetros
        desnivel_m: Desnivel positivo en metros
        peso_kg: Peso del corredor en kg (default: 70)
    
    Returns:
        Calorías estimadas (int)
    """
    # Calorías base por km de trail: ~70 cal/km para persona de 70kg
    calorias_base = distancia_km * peso_kg
    
    # Calorías adicionales por desnivel: ~0.5 cal por metro y kg
    calorias_desnivel = desnivel_m * peso_kg * 0.5
    
    return int(calorias_base + calorias_desnivel)


def comparar_etapas(etapas):
    """
    Compara las métricas de diferentes etapas.
    
    Args:
        etapas: Lista de diccionarios con datos de etapas
    
    Returns:
        Dict con comparaciones
    """
    comparacion = {
        "mas_larga": max(etapas, key=lambda x: x["distancia_km"]),
        "mas_desnivel": max(etapas, key=lambda x: x["desnivel_positivo"]),
        "mas_desnivel_por_km": max(
            etapas, 
            key=lambda x: x["desnivel_positivo"] / x["distancia_km"]
        ),
    }
    return comparacion


def formato_tiempo(horas):
    """
    Formatea tiempo en horas a formato HH:MM.
    
    Args:
        horas: Tiempo en horas (float)
    
    Returns:
        String en formato "Xh YYmin"
    """
    h = int(horas)
    m = int((horas - h) * 60)
    return f"{h}h {m:02d}min"