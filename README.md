# MyGit
Scouting for profiles Github

🛠️ Guía de Instalación y Configuración (Backend/Core)

Se recomienda utilizar Python 3.11.

1. Configurar el entorno virtual (venv)
Es importante usar un entorno virtual para mantener las dependencias aisladas del sistema.
Windows
```bash
python -m venv venv.\venv\Scripts\activate
```
Linux / Mac
```bash
python3 -m venv venvsource venv/bin/activate
```

2. Instalar dependencias
Con el entorno virtual activado ((venv) visible en la terminal), instalar las dependencias del proyecto:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno
Dentro de la carpeta core/ se incluye un archivo .env.example con un ejemplo de configuración para crear el archivo .env. (para mas info buscar en .env.example)

4. Levantar el servidor de desarrollo
Ejecutar la API con recarga automática (hot-reload):
```bash
uvicorn app.main:app --reload
```
La API quedará disponible en:
```bash
http://127.0.0.1:8000
```