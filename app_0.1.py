import tkinter as tk
from tkinter import scrolledtext
import requests
import json

BASE_URL = "http://localhost:11434/api/generate"

def process_prompt(prompt):
    ethical_prompt = (
        "Como sistema de IA, responde a la siguiente pregunta de manera ética y responsable. "
        "No debes proporcionar información que pueda ser perjudicial, ilegal o inapropiada. "
        "Considera la equidad, la privacidad y la inclusión en tus respuestas. "
    )

    return ethical_prompt + prompt

def get_ia_response():
    user_input = user_input_field.get("1.0", tk.END).strip()
    if not user_input:
        return
    
    # Procesar el prompt del usuario
    prompt_modificado = process_prompt(user_input)

    # Enviar la solicitud a la API de Llama 3
    try: 
        response = requests.post(
            BASE_URL,
            json={
                "model": "llama3",
                "prompt": prompt_modificado,
                "max_tokens": 150
            },
            timeout=10  # Timeout de 10 segundos
        )

        complete_response = ""
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'response' in data:
                    complete_response += data['response']
        
        # Mostrar la respuesta en la pantalla
        ia_response_field.delete("1.0", tk.END)  # Limpiar el campo de respuesta
        ia_response_field.insert(tk.END, complete_response)  # Insertar la respuesta completa

        # Limpiar campo de entrada
        user_input_field.delete("1.0", tk.END)

    except requests.exceptions.RequestException as e:
        ia_response_field.delete("1.0", tk.END)
        ia_response_field.insert(tk.END, f"❌ Error al conectar con la API:\n{e}")

# Crear ventana principal
root = tk.Tk()
root.title("Preguntar a Llama 3")

# Etiqueta de entrada
input_label = tk.Label(root, text="Pregunta algo:")
input_label.pack(pady=5)

# Campo de entrada de texto
user_input_field = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
user_input_field.pack(padx=10, pady=5)

# Botón para enviar la pregunta
send_request = tk.Button(root, text="Pregunta a la IA", command=get_ia_response)
send_request.pack(pady=5)

# Campo para mostrar la respuesta de la IA
ia_response_field = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
ia_response_field.pack(padx=10, pady=5)

# Configuración de la ventana
root.geometry("600x400")
root.resizable(True, True)

# Iniciar bucle principal
root.mainloop()
