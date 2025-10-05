"""
Datos oficiales de altimetría de El Cruce Saucony 2025
Extraídos de las imágenes oficiales publicadas por la organización
"""

# ETAPA 1: 31K, +1600m desnivel
ETAPA_1 = {
    "nombre": "Etapa 1",
    "distancia_km": 31,
    "desnivel_positivo": 1600,
    "inicio": "Largada en Olas",
    "fin": "Campamento 1",
    "oasis": [
        {"nombre": "Oasis A", "km": 7},
        {"nombre": "Oasis B", "km": 16},
        {"nombre": "Oasis C", "km": 23},
    ],
    # Perfil de altimetría (km, altitud_m)
    "perfil": [
        (0, 1000), (2, 1100), (4, 1250), (6, 1400), (8, 1550),
        (10, 1750), (12, 1800), (14, 1700), (16, 1600), (18, 1200),
        (20, 1100), (22, 1150), (24, 1200), (26, 1100), (28, 1050),
        (30, 1000), (31, 1000)
    ],
    "caracteristicas": "Etapa más técnica con ascenso fuerte hasta 1800m en los primeros 12km"
}

# ETAPA 2: 32K, +1300m desnivel
ETAPA_2 = {
    "nombre": "Etapa 2",
    "distancia_km": 32,
    "desnivel_positivo": 1300,
    "inicio": "Campamento 1",
    "fin": "Campamento 2",
    "oasis": [
        {"nombre": "Oasis D", "km": 11},
        {"nombre": "Oasis E", "km": 23},
    ],
    # Perfil de altimetría (km, altitud_m)
    "perfil": [
        (0, 1000), (2, 1100), (4, 1200), (6, 1300), (8, 1250),
        (10, 1200), (12, 1300), (14, 1200), (16, 1100), (18, 1000),
        (20, 1100), (22, 1050), (24, 1000), (26, 1100), (28, 1050),
        (30, 1000), (32, 950)
    ],
    "caracteristicas": "Perfil ondulado con múltiples subidas y bajadas moderadas"
}

# ETAPA 3: 30K, +1500m desnivel
ETAPA_3 = {
    "nombre": "Etapa 3",
    "distancia_km": 30,
    "desnivel_positivo": 1500,
    "inicio": "Largada 3 (Campamento 2)",
    "fin": "Centro Villa La Angostura",
    "oasis": [
        {"nombre": "Oasis F", "km": 5},
        {"nombre": "Oasis G", "km": 22},
    ],
    # Perfil de altimetría (km, altitud_m)
    "perfil": [
        (0, 1000), (2, 1100), (4, 1200), (6, 1300), (8, 1400),
        (10, 1500), (12, 1600), (14, 1700), (16, 1800), (18, 1650),
        (20, 1400), (22, 1200), (24, 1000), (26, 900), (28, 850),
        (30, 800)
    ],
    "caracteristicas": "Gran ascenso en la primera mitad hasta 1800m, luego descenso prolongado"
}

# Resumen general del evento
RESUMEN_EVENTO = {
    "nombre": "El Cruce Saucony 2025",
    "ubicacion": "Villa La Angostura, Neuquén, Argentina",
    "fechas": "1-7 Diciembre 2025",
    "distancia_total_km": 93,
    "desnivel_total_positivo": 4400,
    "num_etapas": 3,
    "num_campamentos": 2,
    "num_oasis": 7,
    "tiempo_limite_min_km": 15,
}

# Lista de todas las etapas
ETAPAS = [ETAPA_1, ETAPA_2, ETAPA_3]