import tkinter as tk
import threading
import speech_recognition as sr
import random
import webbrowser

# Lista de hashtags relacionados
tags = [
    '#BabyClothes', '#BabyFashion', '#BabyStyle', '#BabyOOTD', '#BabyLove', '#BabyGram',
    '#SleepingBaby', '#BabySleep', '#BabyNaps', '#SleepyBaby', '#SleepingBeauty', '#NapTime',
    '#PregnantBelly', '#BellyPregnant', '#PregnancyBellyProgress', '#BabyBumpJourney',
    '#PregnancyBellyGrowth', '#BumpUpdate', '#PregnancyProgress', '#MaternityJourney',
    '#GrowingWithLove', '#BabyBumpTransformation', '#PregnancyBellyWatch', '#BumpWatch',
    '#RopaDeBebé', '#ModaDeBebé', '#EstiloDeBebé', '#AmorDeBebé', '#HoraDeDormir', '#SueñoDeBebé',
    '#BarrigaEmbarazada', '#ProgresoBarrigaEmbarazada', '#ViajeDeLaBarrigaDelBebé', '#CrecimientoBarrigaEmbarazada',
    '#ActualizaciónDeLaBarriga', '#ProgresoEmbarazo', '#ViajeDeMaternidad', '#CreciendoConAmor',
    '#TransformaciónDeLaBarrigaDelBebé', '#ObservaciónDeLaBarrigaEmbarazada', '#ObservaciónDeLaBarriga',
]

# Variable de control para detener la grabación
running = True
tag_recomendado = None

# Configurar la interfaz gráfica
ventana = tk.Tk()
ventana.title("Transcriptor de Voz")
ventana.geometry("500x300")

# Área de texto para mostrar la transcripción
texto_transcripcion = tk.Text(ventana, wrap="word", height=15)
texto_transcripcion.pack(padx=10, pady=10)

# Botón para detener la transcripción
boton_colgar = tk.Button(ventana, text="Detener", command=lambda: detener_transcripcion(), fg="white", bg="red")
boton_colgar.pack(pady=10)

# Función de transcripción de voz
def transcribir_voz():
    global running, tag_recomendado
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando en tiempo real...")
        while running:
            try:
                audio_data = recognizer.listen(source, timeout=7, phrase_time_limit=7)
                text = recognizer.recognize_google(audio_data, language='es-ES')

                # Insertar el texto en la interfaz de manera segura
                ventana.after(0, lambda: texto_transcripcion.insert(tk.END, text + '\n'))
                ventana.after(0, lambda: texto_transcripcion.see(tk.END))

                # Verificar si se mencionan "embarazo" o "embarazada"
                if 'embarazo' in text.lower() or 'embarazada' in text.lower():
                    tag_recomendado = random.choice(tags)
            except sr.UnknownValueError:
                ventana.after(0, lambda: texto_transcripcion.insert(tk.END, "No pude entender el audio.\n"))
                ventana.after(0, lambda: texto_transcripcion.see(tk.END))
            except sr.RequestError:
                ventana.after(0, lambda: texto_transcripcion.insert(tk.END, "Error al conectarse al servicio de reconocimiento de voz.\n"))
                ventana.after(0, lambda: texto_transcripcion.see(tk.END))
            except sr.WaitTimeoutError:
                ventana.after(0, lambda: texto_transcripcion.insert(tk.END, "Tiempo de espera agotado al escuchar.\n"))
                ventana.after(0, lambda: texto_transcripcion.see(tk.END))

# Función para detener la transcripción y abrir la página o mostrar un mensaje
def detener_transcripcion():
    global running, tag_recomendado
    running = False
    if tag_recomendado:
        webbrowser.open(f'https://www.instagram.com/explore/tags/{tag_recomendado.strip("#")}')
        print(f"Se ha detenido la escucha y se abrió la página con el tag: {tag_recomendado}")
    else:
        print("No podemos recomendar nada.")
    ventana.quit()

# Ejecutar la transcripción en un hilo separado
hilo_transcripcion = threading.Thread(target=transcribir_voz)
hilo_transcripcion.start()

# Iniciar la interfaz gráfica
ventana.mainloop()
