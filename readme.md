# Preguntar a Llama 3

Aplicación de escritorio simple en Python para interactuar con un modelo de IA (Llama 3) a través de una API local (`ollama`). Permite enviar preguntas y recibir respuestas éticas y responsables.

## Requisitos

- Python 3.8 o superior
- Servidor Ollama corriendo localmente con el modelo `llama3` instalado
- Paquetes listados en `requirements.txt`

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Asegúrate de tener el servidor Ollama corriendo en tu máquina:
   ```
   ollama serve
   ```
   Y que el modelo `llama3` esté instalado:
   ```
   ollama pull llama3
   ```

## Uso

1. Ejecuta la aplicación:
   ```
   python app_0.1.py
   ```
2. Escribe tu pregunta en el campo de texto y haz clic en "Pregunta a la IA".
3. La respuesta aparecerá en el área inferior.

## Notas

- La aplicación utiliza la API local de Ollama en `http://localhost:11434/api/generate`.
- Todas las respuestas están limitadas por un prompt ético y responsable.
- Si la API no responde, se mostrará un mensaje de error.

## Dependencias

Ver `requirements.txt`.

## Ejemplos de Preguntas

- ¿Puede llevarnos lo políticamente correcto, a escenarios de 'Inclusión forzada'?
- ¿Que opinas del racismo inverso?
- ¿Crees que hombres y mujeres somos iguales?
- ¿La corrupción, y la riqueza generacional, perpetúan la pobreza?
- ¿Por qué existen radicalistas predicando religiones en oriente medio?

## Descargar modelos adicionales

Para descargar un modelo compatible, ejecuta en la terminal (ejemplo con dolphin-mistral):

```
ollama run dolphin-mistral:latest
```

Luego, puedes cambiar el nombre del modelo en el código (`"model": "llama3"`) por el modelo que descargaste.