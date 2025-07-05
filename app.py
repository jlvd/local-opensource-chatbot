import customtkinter as ctk
import requests
import json
import subprocess
import os
from datetime import datetime

# Configuración de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_URL = "http://localhost:11434/api/generate"
HISTORIAL_FILE = "historial.json"

def get_installed_models():
    """
    Ejecuta 'ollama list' y devuelve una lista de modelos instalados.
    """
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, check=True
        )
        models = []
        for line in result.stdout.strip().splitlines()[1:]:  # Omitir cabecera
            parts = line.split()
            if parts:
                models.append(parts[0])  # Primer campo = nombre modelo
        return models if models else ["ERROR AL OBTENER MODELOS"]
    except Exception as e:
        print("⚠️ Error al obtener modelos:", e)
        return ["ERROR AL OBTENER MODELOS"]

def process_prompt(user_input):
    ethical_prompt = (
        "Como sistema de IA, asegurate de que tus respuestas sean imparciales, éticas y cumplan con las regulaciones de la IA. "
        "Considera la equidad, la privacidad y la inclusión en tu respuesta. "
        "Por favor no respondas a preguntas que puedan ser censuradas por su contenido. "
        "Tus mensajes no deben ser mayores de doscientas palabras. "
        "Todas tus respuestas deben ser en Español.\n\n"
    )
    return ethical_prompt + user_input

def save_to_history(question, question_time, response, response_time, model_name):
    """
    Guarda la pregunta y respuesta con sus fechas en un archivo JSON.
    """
    entry = {
        "modelo": model_name,
        "pregunta": {
            "texto": question,
            "fecha_hora": question_time
        },
        "respuesta": {
            "texto": response,
            "fecha_hora": response_time
        }
    }
    historial = []

    # Leer historial anterior si existe
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except json.JSONDecodeError:
            historial = []  # Si el archivo está corrupto, empezar desde cero

    # Agregar nueva entrada
    historial.append(entry)

    # Guardar al archivo
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def get_ai_response():
    user_input = user_input_field.get("1.0", "end").strip()
    model = selected_model.get()
    response_display.delete("1.0", "end")  # Limpiar respuestas anteriores
    
    # Validar entrada del usuario
    if not user_input:
        response_display.insert("end", "⚠️ Por favor escribe una pregunta.\n")
        return
    
    # Validar modelo seleccionado
    if model == "ERROR AL OBTENER MODELOS":
        response_display.insert("end", "⚠️ No se pudo obtener la lista de modelos instalados.\n")
        return

    question_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_button.configure(state="disabled", text="⏳ Esperando...")
    response_display.insert("end", f"⏳ Consultando IA ({model})...\n")
    response_display.see("end")
    root.update()  # Actualizar la interfaz

    modified_prompt = process_prompt(user_input)

    try:
        response = requests.post(
            BASE_URL,
            json={
                "model": model,
                "prompt": modified_prompt,
                "max_tokens": 150
            },
            timeout=60
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        response_display.insert("end", f"❌ Error al conectar con la IA: {e}\n")
        send_button.configure(state="normal", text="🚀 Respondeme")
        return

    complete_response = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            data = json.loads(line)
            if "response" in data:
                complete_response += data["response"]

    response_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if complete_response:
        response_display.insert("end", f"🤖 {model}: {complete_response.strip()}\n\n")
        # Guardar en historial con fechas
        save_to_history(user_input, question_time, complete_response.strip(), response_time, model)
    else:
        response_display.insert("end", "⚠️ No se recibió respuesta de la IA.\n")

    send_button.configure(state="normal", text="🚀 Respondeme")

# Crear ventana principal
root = ctk.CTk()
root.title("💡 Preguntar a Modelos IA OpenSource")
root.geometry("800x700")
root.resizable(False, False)

# Variable para el modelo seleccionado
selected_model = ctk.StringVar()

# Etiqueta de entrada
input_label = ctk.CTkLabel(root, text="💬 Pregunta algo:", font=ctk.CTkFont(size=16, weight="bold"))
input_label.pack(pady=(20, 10))

# Campo de entrada de texto
user_input_field = ctk.CTkTextbox(root, width=700, height=150, font=ctk.CTkFont(size=14))
user_input_field.pack(pady=10)

# Menú desplegable para modelos
model_label = ctk.CTkLabel(root, text="🤖 Modelo IA:", font=ctk.CTkFont(size=14))
model_label.pack(pady=(15, 5))

models = get_installed_models()
selected_model.set(models[0])  # Selecciona el primero por defecto
model_dropdown = ctk.CTkOptionMenu(root, values=models, variable=selected_model)
model_dropdown.pack(pady=(0, 15))

# Botón para enviar pregunta
send_button = ctk.CTkButton(root, text="🚀 Respondeme", font=ctk.CTkFont(size=14, weight="bold"), command=get_ai_response)
send_button.pack(pady=10)

# Campo para mostrar respuestas
response_display = ctk.CTkTextbox(root, width=700, height=300, font=ctk.CTkFont(size=13))
response_display.pack(pady=10)
response_display.configure(state="normal")

# Ejecutar la aplicación
root.mainloop()
