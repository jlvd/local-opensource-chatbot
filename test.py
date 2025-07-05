
import re

def clean_response(text):
    """
    Quita todas las ocurrencias del bloque <think>...</think> (incluyendo etiquetas y contenido interno).
    """
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return cleaned.strip()

texto = "<think>Estoy pensando en la respuesta.</think> Ahora va la respuesta final."
print(clean_response(texto))
# Salida: "Ahora va la respuesta final."
