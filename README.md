# MyGit
Scouting for profiles Github

# 🛠️ Guía de Instalación y Configuración

Se recomienda utilizar Docker Desktop para evitar problemas de entorno, dependencias y versiones de Python. (No es necesario usar un entorno virtual)

---

# 📦 Requisitos

Instalar:

- Docker Desktop
- Git
- pip actualizado
- Node.js
- npm

Verificar instalación:

```bash
docker --version
```
```bash
docker compose version
```
```bash
node --version
```
```bash
npm --version
```
---

#  🚀 Levantar Backend/Core

Desde la raíz del proyecto ejecutar:
```bash
docker compose up -d --build
```
La primera ejecución puede tardar unos minutos porque Docker descarga las imágenes y dependencias necesarias.

---

#  🌐 Acceso a la API

La API quedará disponible en:
```bash
http://127.0.0.1:8000
```

---

#  🖥️ Levantar Frontend/UI

Desde la raíz del proyecto entrar a la carpeta `ui`:
```bash
cd ui
```

Instalar dependencias:
```bash
npm install
```

Verificar que exista el archivo `.env` con la URL del backend:
```bash
VITE_API_URL=http://localhost:8000
```

Levantar el servidor de desarrollo:
```bash
npm run dev
```

---

#  🌐 Acceso al Frontend

La aplicación quedará disponible en:
```bash
http://localhost:5173
```
