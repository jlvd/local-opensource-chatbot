import json
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

# Archivo historial
HISTORIAL_FILE = "historial.json"

# Cargar datos del historial
with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
    historial = json.load(f)

# Diccionario para agrupar por modelo
stats = defaultdict(lambda: {"tiempos": [], "longitudes_caracteres": [], "longitudes_palabras": []})

# Analizar cada entrada
for entry in historial:
    modelo = entry.get("modelo", "desconocido")
    
    # Fechas
    pregunta_time = entry["pregunta"]["fecha_hora"]
    respuesta_time = entry["respuesta"]["fecha_hora"]

    # Convertir a objetos datetime
    pregunta_dt = datetime.strptime(pregunta_time, "%Y-%m-%d %H:%M:%S")
    respuesta_dt = datetime.strptime(respuesta_time, "%Y-%m-%d %H:%M:%S")

    # Calcular tiempo de respuesta en segundos
    tiempo_respuesta = (respuesta_dt - pregunta_dt).total_seconds()
    stats[modelo]["tiempos"].append(tiempo_respuesta)

    # Calcular longitud de la respuesta en caracteres y palabras
    respuesta_texto = entry["respuesta"]["texto"]
    longitud_caracteres = len(respuesta_texto)
    longitud_palabras = len(respuesta_texto.split())

    stats[modelo]["longitudes_caracteres"].append(longitud_caracteres)
    stats[modelo]["longitudes_palabras"].append(longitud_palabras)

# Calcular promedios por modelo
modelos = []
tiempos_promedio = []
longitudes_promedio = []
palabras_promedio = []

print("📊 Análisis de tiempos de respuesta y longitud por modelo:\n")
for modelo, datos in stats.items():
    tiempos = datos["tiempos"]
    longitudes_c = datos["longitudes_caracteres"]
    longitudes_p = datos["longitudes_palabras"]

    promedio_tiempo = sum(tiempos) / len(tiempos)
    promedio_longitud_c = sum(longitudes_c) / len(longitudes_c)
    promedio_longitud_p = sum(longitudes_p) / len(longitudes_p)

    modelos.append(modelo)
    tiempos_promedio.append(promedio_tiempo)
    longitudes_promedio.append(promedio_longitud_c)
    palabras_promedio.append(promedio_longitud_p)

    print(f"🔹 Modelo: {modelo}")
    print(f"   ⏱️ Tiempo medio de respuesta: {promedio_tiempo:.2f} segundos")
    print(f"   📝 Longitud media de respuesta: {promedio_longitud_c:.2f} caracteres")
    print(f"   🗨️ Longitud media de respuesta: {promedio_longitud_p:.2f} palabras")
    print(f"   📄 Total de consultas: {len(tiempos)}\n")

# --- Gráfico de barras ---
fig, ax1 = plt.subplots(figsize=(10, 6))

# Colores distintos para cada métrica
color1 = 'tab:blue'
color2 = 'tab:orange'

# Barras para tiempo de respuesta
ax1.bar(modelos, tiempos_promedio, color=color1, width=0.4, label='⏱️ Tiempo medio (s)')
ax1.set_ylabel('Tiempo medio de respuesta (segundos)', color=color1, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xlabel('Modelos IA', fontsize=12)

# Segundo eje Y para longitud de respuesta (caracteres)
ax2 = ax1.twinx()
ax2.bar([m + " " for m in modelos], longitudes_promedio, color=color2, width=0.4, label='📝 Longitud media')
ax2.set_ylabel('Longitud media de respuesta (caracteres)', color=color2, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color2)

# Título y leyenda
plt.title('⏳ Tiempo de Respuesta y Longitud por Modelo', fontsize=14)
fig.tight_layout()
plt.show()
