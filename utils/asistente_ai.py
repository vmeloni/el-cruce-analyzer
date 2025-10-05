"""
Asistente de IA con OpenAI para El Cruce Analyzer
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def crear_contexto_etapas(etapas):
    """
    Crea un contexto con información de las etapas para el asistente.
    """
    contexto = "Información de El Cruce Saucony 2025:\n\n"
    
    for etapa in etapas:
        contexto += f"{etapa['nombre']}:\n"
        contexto += f"- Distancia: {etapa['distancia_km']}km\n"
        contexto += f"- Desnivel positivo: {etapa['desnivel_positivo']}m\n"
        contexto += f"- Intensidad: {etapa['desnivel_positivo']/etapa['distancia_km']:.1f} m/km\n"
        contexto += f"- Inicio: {etapa['inicio']}\n"
        contexto += f"- Fin: {etapa['fin']}\n"
        contexto += f"- Características: {etapa['caracteristicas']}\n"
        contexto += f"- Oasis: {len(etapa['oasis'])} puntos\n\n"
    
    return contexto


def generar_respuesta_asistente(pregunta_usuario, etapas, historial=[]):
    """
    Genera una respuesta del asistente usando GPT-4.
    
    Args:
        pregunta_usuario: La pregunta del usuario
        etapas: Lista de datos de etapas
        historial: Lista de mensajes previos (opcional)
    
    Returns:
        Respuesta del asistente
    """
    
    # Sistema de prompt
    system_prompt = f"""Eres un asistente experto en trail running y entrenamiento para carreras de montaña.
Tu especialidad es ayudar a corredores a prepararse para El Cruce Saucony 2025, una carrera por etapas de 3 días 
en la Patagonia Argentina.

{crear_contexto_etapas(etapas)}

IMPORTANTE:
- Da consejos prácticos y específicos basados en los datos de las etapas
- Considera las características únicas de cada etapa
- Sé conciso pero completo en tus respuestas
- Si preguntan sobre entrenamiento, considera los desniveles y distancias específicas
- Si preguntan sobre estrategia de carrera, usa los datos de altimetría
- Si preguntan sobre nutrición/hidratación, considera la ubicación de los oasis
- Tiempo límite: 15 min/km por etapa
- Formato: Usa markdown para estructura (listas, negritas, etc.)
"""
    
    # Construir mensajes
    mensajes = [{"role": "system", "content": system_prompt}]
    
    # Agregar historial si existe
    mensajes.extend(historial)
    
    # Agregar pregunta actual
    mensajes.append({"role": "user", "content": pregunta_usuario})
    
    try:
        # Llamada a OpenAI
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo más económico
            messages=mensajes,
            temperature=0.7,
            max_tokens=800
        )
        
        return respuesta.choices[0].message.content
    
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"


def generar_plan_entrenamiento(semanas_disponibles, nivel_actual, objetivo_pace, etapas):
    """
    Genera un plan de entrenamiento personalizado.
    """
    
    prompt = f"""Genera un plan de entrenamiento de {semanas_disponibles} semanas para El Cruce Saucony 2025.

Perfil del corredor:
- Nivel actual: {nivel_actual}
- Objetivo de pace: {objetivo_pace} min/km
- Etapas a completar: 3 días consecutivos, ~93km totales, +4,400m desnivel

Estructura el plan por semanas con:
1. Objetivo de la semana
2. Días de entrenamiento (tipo y duración)
3. Desnivel acumulado semanal objetivo
4. Punto clave a trabajar

Sé específico y progresivo. Considera que necesitan entrenar:
- Resistencia aeróbica
- Fuerza en piernas
- Técnica de subida/bajada
- Adaptación a desnivel acumulado
"""
    
    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": crear_contexto_etapas(etapas)},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return respuesta.choices[0].message.content
    
    except Exception as e:
        return f"Error al generar plan: {str(e)}"