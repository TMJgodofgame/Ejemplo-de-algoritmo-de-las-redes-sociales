import random
import webbrowser
import os
import sqlite3
import csv
from datetime import datetime, timedelta

# Construir la ruta a la base de datos del historial de Edge de forma dinámica
user_profile = os.environ['USERPROFILE']
history_db_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'History')


# Función para convertir el timestamp de Chrome a una fecha legible
def convertir_fecha_chrome(timestamp):
    if timestamp:
        epoch_start = datetime(1601, 1, 1)
        delta = timedelta(microseconds=timestamp)
        return epoch_start + delta
    return None


# Conexión al archivo de base de datos de Edge
conn = sqlite3.connect(history_db_path)
cursor = conn.cursor()

# Consulta para obtener el historial
cursor.execute("SELECT title, visit_count, last_visit_time FROM urls")

# Escritura en un archivo CSV
csv_filename = 'historial_edge.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Título', 'Visitas', 'Última Visita'])
    for row in cursor.fetchall():
        title, visit_count, last_visit_time = row
        fecha_legible = convertir_fecha_chrome(last_visit_time)
        writer.writerow([title, visit_count, fecha_legible])

# Cierre de la conexión
conn.close()

# Lectura e impresión del contenido del archivo CSV en la terminal y búsqueda de palabras clave
encontrado = False
with open(csv_filename, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Saltar la cabecera
    for row in reader:
        titulo = row[0]
        if len(titulo) < 150:
            print(titulo)
        if 'embarazo' in titulo.lower() or 'embarazada' in titulo.lower():
            encontrado = True

# Si se encuentran las palabras clave, proceder con la generación de etiquetas
if encontrado:
    # Lista original de etiquetas
    tags = [
        '#BabyClothes', '#BabyFashion', '#BabyStyle', '#BabyOOTD', '#BabyLove', '#BabyGram',
        '#SleepingBaby', '#BabySleep', '#BabyNaps', '#SleepyBaby', '#SleepingBeauty', '#NapTime',
        '#PregnantBelly', '#BellyPregnant', '#PregnancyBellyProgress', '#BabyBumpJourney',
        '#PregnancyBellyGrowth', '#BumpUpdate', '#PregnancyProgress', '#MaternityJourney',
        '#GrowingWithLove', '#BabyBumpTransformation', '#PregnancyBellyWatch', '#BumpWatch'
    ]

    # Elegir un tag aleatorio
    tage = random.choice(tags).strip("#").replace(" ", "")

    # Abrir la página de Instagram con el tag elegido
    webbrowser.open(f'https://www.instagram.com/explore/tags/{tage}')
