# MyGit
Scouting for profiles Github

# 🛠️ Guía de Instalación y Configuración (Backend/Core)

Se recomienda utilizar Docker Desktop para evitar problemas de entorno, dependencias y versiones de Python. (No es necesario usar un entorno virtual)

---

# 📦 Requisitos

Instalar:

- Docker Desktop
- Git
- pip actualizado

Verificar instalación:

```bash
docker --version
```
```bash
docker compose version
```
---

#  🚀 Levantar el proyecto

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