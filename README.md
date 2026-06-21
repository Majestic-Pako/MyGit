<div align="center">

# >_ MyGit

### Scouting for GitHub profiles

![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-42B883?style=for-the-badge&logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub API](https://img.shields.io/badge/GitHub_API-181717?style=for-the-badge&logo=github&logoColor=white)

</div>

## > presentación

MyGit es una aplicación web para buscar y analizar perfiles públicos de GitHub.

Permite visualizar información general del usuario, repositorios, lenguajes utilizados, colaboradores y métricas principales desde un dashboard simple y directo.

## > stack

| Área          | Tecnologías             |
| ------------- | ----------------------- |
| Backend       | Python · FastAPI        |
| Frontend      | Vue · Vite              |
| Base de datos | MySQL                   |
| Entorno       | Docker · Docker Compose |
| API externa   | GitHub API              |

## > requisitos

* Docker Desktop
* Git
* Node.js
* npm

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

## > configuración

### Backend/Core

Debe existir:

```txt
core/.env
```

Puede copiarse desde el archivo de ejemplo:

```bash
cp core/.env.example core/.env
```

En Windows PowerShell:

```powershell
Copy-Item core\.env.example core\.env
```

Variables principales:

```env
DB_HOST=database
DB_PORT=3306
DB_NAME=MyGitDB
DB_USER=root
DB_PASSWORD=root
GITHUB_TOKEN=tu_token_de_github
```

`GITHUB_TOKEN` es opcional, pero se recomienda configurarlo para aumentar el límite de consultas a la API de GitHub.

### Frontend/UI

Debe existir:

```txt
ui/.env
```

Contenido:

```env
VITE_API_URL=http://localhost:8000
```

## > levantar backend + base de datos

Desde la raíz del proyecto:

```bash
docker compose up -d --build
```

Este comando levanta:

* Backend/Core con FastAPI.
* Base de datos MySQL.
* Script inicial ubicado en `db/MyGitDB.sql`.

Comandos útiles:

```bash
docker compose ps
```

```bash
docker compose logs -f backend
```

```bash
docker compose logs -f database
```

```bash
docker compose down
```

```bash
docker compose down -v
```

`docker compose down -v` elimina los datos locales de MySQL. Debe usarse solo para reiniciar la base completamente.

## > verificar base de datos

Entrar a MySQL:

```bash
docker compose exec database mysql -uroot -proot MyGitDB
```

Comandos útiles dentro de MySQL:

```sql
SHOW TABLES;
```

```sql
SELECT COUNT(*) FROM users;
```

```sql
SELECT COUNT(*) FROM github_profiles;
```

## > levantar frontend/ui

```bash
cd ui
```

```bash
npm install
```

```bash
npm run dev
```

## > accesos

| Servicio  | URL                             |
| --------- | ------------------------------- |
| Frontend  | http://localhost:5173           |
| API       | http://127.0.0.1:8000           |
| Swagger   | http://127.0.0.1:8000/docs      |
| Health DB | http://127.0.0.1:8000/db/health |

## > estructura

```txt
MyGit/
├── core/                 # Backend FastAPI
├── db/                   # Script SQL
├── ui/                   # Frontend Vue
├── docker-compose.yml
└── README.md
```
