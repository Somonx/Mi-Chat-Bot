import moviepy.editor as mp
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import words
import nltk

# Descargar recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('words')

# Función para extraer la transcripción de un video local
def transcripcion_video_local(nombre_archivo):
    clip = mp.VideoFileClip(nombre_archivo)
    clip.audio.write_audiofile(r"audio_extraido.wav")

    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile("audio_extraido.wav")

    with audio_file as source:
        audio = recognizer.record(source)

    texto_transcrito = recognizer.recognize_google(audio, language="es-ES")
    return texto_transcrito

# Función para contar palabras acentuadas en el texto
def contar_palabras_acentuadas(transcripcion):
    palabras = word_tokenize(transcripcion.lower(), language='spanish')
    esdrujulas = []
    agudas = []
    llanas = []

    for palabra in palabras:
        if palabra in words.words():
            if len(palabra) >= 2:
                if palabra[-1] in 'áéíóú':
                    esdrujulas.append(palabra)
                elif palabra[-1] in 'aeiouáéíóú' and palabra[-2] not in 'aeiouáéíóú':
                    agudas.append(palabra)
                else:
                    llanas.append(palabra)
            else:
                llanas.append(palabra)

    return {
        'esdrújulas': len(esdrujulas),
        'agudas': len(agudas),
        'llanas': len(llanas)
    }

# Función principal del chatbot
def main():
    nombre_video = input("Ingrese el nombre del archivo de video local (incluya la extensión): ")
    transcripcion = transcripcion_video_local(nombre_video)
    conteo_palabras_acentuadas = contar_palabras_acentuadas(transcripcion)

    print("\nTranscripción del video:\n", transcripcion)
    print("\nResultados del análisis de palabras acentuadas:")
    print("Palabras esdrújulas:", conteo_palabras_acentuadas['esdrújulas'])
    print("Palabras agudas:", conteo_palabras_acentuadas['agudas'])
    print("Palabras llanas:", conteo_palabras_acentuadas['llanas'])

# Ejecución del chatbot
if __name__ == "__main__":
    main()
