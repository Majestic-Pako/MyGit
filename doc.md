# Documentación técnica · MyGit

Documentación complementaria del proyecto MyGit con tecnologías, arquitectura, patrones, base de datos, endpoints, configuración y alcance técnico.

| Proyecto      | MyGit          |
| ------------- | -------------- |
| Backend       | FastAPI        |
| Frontend      | Vue            |
| Base de datos | MySQL          |
| Entorno       | Docker Compose |
| API externa   | GitHub API     |

---

## Índice

* [Resumen ejecutivo](#resumen-ejecutivo)
* [Tecnologías principales](#tecnologías-principales)
* [Librerías y dependencias](#librerías-y-dependencias)
* [Arquitectura general](#arquitectura-general)
* [Patrones de diseño](#patrones-de-diseño)
* [Base de datos](#base-de-datos)
* [Funcionalidades](#funcionalidades)
* [Seguridad y configuración](#seguridad-y-configuración)
* [Estructura de carpetas](#estructura-de-carpetas)
* [Endpoints](#endpoints)
* [Comandos útiles](#comandos-útiles)
* [Observaciones y pendientes](#observaciones-y-pendientes)

---

## Resumen ejecutivo

MyGit es una aplicación web para analizar perfiles públicos de GitHub. Su implementación combina:

* Backend REST con Python, FastAPI y Uvicorn.
* Frontend SPA con Vue 3, Vue Router y Vite.
* Consumo de la API REST pública de GitHub.
* Caché persistente en archivos JSON y persistencia complementaria en MySQL 8.
* Registro e inicio de sesión simple contra MySQL.
* Docker Compose para levantar el backend y la base de datos.
* Frontend cercano a MVVM y backend organizado por capas.
* Patrones Adapter, Repository, Service y Strategy.

### Estado general

* La consulta y el análisis de perfiles están implementados.
* El dashboard, los lenguajes, los repositorios y los colaboradores usan datos reales.
* La autenticación básica está implementada, pero no crea una sesión segura en el servidor.
* MySQL recibe datos analizados, pero no recupera los perfiles consultados.
* El historial visible se guarda en `localStorage`, no en `search_history`.
* Las vistas Perfil y Métricas son placeholders.
* No se encontraron pruebas automatizadas.
* No se modificó ningún archivo durante el relevamiento original.

---

## Tecnologías principales

### Backend

| Tecnología                | Uso                                                        |
| ------------------------- | ---------------------------------------------------------- |
| Python 3.11               | Lenguaje del backend y versión utilizada en Docker         |
| FastAPI 0.136.1           | API HTTP, routers, validación y documentación automática   |
| Uvicorn 0.46.0            | Servidor ASGI                                              |
| Pydantic                  | Modelado de requests y perfiles; dependencia de FastAPI    |
| HTTPX 0.28.1              | Consumo de la API REST de GitHub                           |
| mysql-connector-python 9.5.0 | Conexión y consultas a MySQL                            |
| python-dotenv 1.2.2       | Carga de variables desde `core/.env`                       |
| Bibliotecas estándar      | PBKDF2, HMAC, JSON, logging, fechas y sincronización        |

Archivos centrales:

* [`main.py`](core/app/main.py)
* [`requirements.txt`](core/app/config/requirements.txt)
* [`DockerFile`](core/app/DockerFile)

No se encontraron `pyproject.toml`, `setup.py`, Poetry ni Pipenv.

### Frontend

| Tecnología           | Uso                                                  |
| -------------------- | ---------------------------------------------------- |
| Vue 3.5.34           | SPA y componentes reactivos                          |
| Composition API      | `ref`, `computed`, `onMounted` y composables         |
| Vue Router 4.6.4     | Navegación entre inicio, login, dashboard e historial|
| Vite 8               | Servidor de desarrollo y compilación                 |
| JavaScript ES Modules| Servicios, viewModels y utilidades                   |
| CSS nativo           | Estilos divididos por pantalla y componente          |
| Lucide               | Iconografía general                                  |
| Iconify              | Iconos de lenguajes                                  |

No se utilizan TypeScript, Pinia, Vuex, Axios ni un framework CSS.

### Base de datos

* MySQL 8.0 con charset `utf8mb4`.
* Esquema inicializado desde [`MyGitDB.sql`](db/MyGitDB.sql).
* Persistencia mediante SQL directo y consultas parametrizadas.
* Sin ORM ni sistema de migraciones.

### Docker y entorno

[`docker-compose.yml`](docker-compose.yml) define dos servicios:

| Servicio   | Función             | Puerto |
| ---------- | ------------------- | ------ |
| `database` | MySQL 8.0           | 3306   |
| `backend`  | Aplicación FastAPI  | 8000   |

Detalles del entorno:

* El frontend no está dockerizado.
* El código del backend se monta en `/app`.
* El SQL se monta en `/docker-entrypoint-initdb.d/`.
* Los datos de MySQL usan el volumen `mygit_db_data`.
* El backend usa `core/.env`.
* `depends_on` ordena el inicio, pero no espera a que MySQL esté saludable.
* No hay health checks declarados en Compose.
* Para ejecución local se recomienda Python 3.11 y se requieren `pip`, Git, Node.js y npm.
* Vite 8 exige Node `^20.19.0` o `>=22.12.0`.

### Variables de entorno

La configuración del backend se carga desde:

* [`infrastructure/settings.py`](core/app/infrastructure/settings.py)
* [`config/settings.py`](core/app/config/settings.py)

| Variable        | Componente | Uso                       |
| --------------- | ---------- | ------------------------- |
| `DB_HOST`       | Backend    | Host de MySQL             |
| `DB_PORT`       | Backend    | Puerto de MySQL           |
| `DB_NAME`       | Backend    | Nombre de la base         |
| `DB_USER`       | Backend    | Usuario de MySQL          |
| `DB_PASSWORD`   | Backend    | Contraseña de MySQL       |
| `GITHUB_TOKEN`  | Backend    | Token opcional de GitHub  |
| `VITE_API_URL`  | Frontend   | URL base del backend      |

Existe [`core/.env.example`](core/.env.example). No se encontró `ui/.env.example`, aunque el frontend requiere `VITE_API_URL`.

---

## Librerías y dependencias

### Backend

#### FastAPI

Se utiliza para crear la API REST, registrar routers, aplicar CORS, validar requests de autenticación mediante Pydantic y generar Swagger en `/docs` y OpenAPI en `/openapi.json`.

#### Uvicorn

Ejecuta la aplicación ASGI. El Dockerfile lo inicia con recarga automática:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

`--reload` es apropiado para desarrollo, no para producción.

#### HTTPX

[`github_adapter.py`](core/app/adapters/github_adapter.py) usa llamadas síncronas mediante `httpx.get()` para consultar:

* Perfil del usuario.
* Repositorios públicos.
* Lenguajes por repositorio.
* Colaboradores por repositorio.

#### python-dotenv y mysql-connector-python

`python-dotenv` carga `core/.env` en ejecuciones locales. El conector de MySQL aporta conexiones, cursores normales y de diccionario, transacciones, consultas parametrizadas y manejo de errores como la duplicación de usuarios.

### Frontend

#### Vue y Vue Router

Vue utiliza Single File Components y `<script setup>`. Las rutas disponibles son:

| Ruta         | Pantalla                 |
| ------------ | ------------------------ |
| `/`          | Landing                  |
| `/login`     | Login y registro         |
| `/dashboard` | Dashboard funcional      |
| `/history`   | Historial funcional      |
| `/profile`   | Placeholder              |
| `/metrics`   | Placeholder              |

#### Vite

Scripts definidos:

| Script    | Comando        |
| --------- | -------------- |
| Desarrollo | `vite`       |
| Build       | `vite build` |
| Preview     | `vite preview` |

`vite.config.js` solo registra el plugin de Vue; no existe un proxy hacia el backend.

#### Lucide, Iconify y lockfile

* `lucide-vue-next`: iconos generales.
* `@iconify/vue`: iconos visuales de lenguajes.
* El lockfile marca `lucide-vue-next 1.0.0` como deprecado y recomienda `@lucide/vue`. No bloquea el funcionamiento, pero constituye deuda técnica.
* `package-lock.json` usa la versión 3 y fija, entre otras, Vue 3.5.34, Vue Router 4.6.4, Iconify 5.0.1 y Vite 8.0.14. Debe conservarse para instalaciones reproducibles.

---

## Arquitectura general

```txt
Frontend Vue
    ↓
Services / ViewModels
    ↓
FastAPI Routers
    ↓
Adapter + Strategies
    ↓
Cache JSON + MySQL
```

La solución sigue una arquitectura cliente-servidor: backend modular por capas y frontend Vue organizado con una variante de MVVM basada en composables. No corresponde a un MVC clásico.

### Backend

El backend combina service layer, repository pattern y ports/adapters simplificado.

| Capa          | Ubicación                    | Responsabilidad |
| ------------- | ---------------------------- | --------------- |
| Routers       | `core/app/routers`           | Interfaz HTTP para GitHub, autenticación y health de MySQL |
| Services      | `core/app/services`          | Ejecución de estrategias y hashing de contraseñas |
| Adapter       | `core/app/adapters`          | Encapsular HTTPX y traducir respuestas de GitHub |
| Schemas       | `core/app/schemas`           | Modelo interno de perfiles, repositorios, lenguajes y colaboradores |
| Strategies    | `core/app/strategies`        | Análisis básico, repositorios, lenguajes y colaboración |
| Persistence   | `core/app/persistence`       | Caché JSON atómica y persistencia transaccional |
| Repositories  | `core/app/repositories`      | Acceso SQL especializado |
| Infrastructure| `core/app/infrastructure`    | Conexión Singleton y configuración técnica |

Solo `UserRepository` está conectado directamente al flujo HTTP actual. Los demás repositorios están preparados, pero el guardado principal usa SQL directo desde `DataRegister`.

### Frontend

```txt
Vue View / Component
        ↓
Composable ViewModel
        ↓
Service
        ↓
Backend REST o localStorage
```

* **Views:** dashboard e historial funcionales; perfil y métricas como placeholders; `Index.vue` como landing.
* **ViewModels:** búsqueda, normalización, métricas visuales, historial local, autenticación y contenido de la landing.
* **Services:** análisis de GitHub, autenticación, estado local del usuario e historial en `localStorage`.
* **Components:** layout, autenticación, resumen de lenguajes y colaboradores.

### Persistencia

La lectura inmediata prioriza el caché JSON. MySQL funciona como persistencia complementaria de escritura y conserva perfiles, repositorios, métricas, lenguajes, colaboradores y snapshots.

### Integración externa

`GitHubAdapter` desacopla la API pública de GitHub del modelo interno de MyGit. El token es opcional y amplía el margen frente al rate limit.

---

## Patrones de diseño

| Patrón       | Archivo o componente      | Uso                                           |
| ------------ | -------------------------- | --------------------------------------------- |
| Singleton    | `DatabaseConnection`       | Compartir el administrador de conexión MySQL  |
| Strategy     | Strategies de análisis     | Separar análisis por responsabilidad          |
| Adapter      | `GitHubAdapter`            | Encapsular la API externa                     |
| Repository   | Repositories SQL           | Separar acceso a datos                        |
| Service Layer| `ProfileAnalyzer`, hashing | Mantener lógica fuera de las rutas            |

### Singleton

[`database.py`](core/app/infrastructure/database.py) implementa `DatabaseConnection` mediante `__new__`, `_instance`, doble comprobación y `threading.Lock`. Los repositories y `DataRegister` obtienen la misma instancia y reutilizan la conexión mientras esté activa.

Una conexión global puede ser suficiente para el estado actual, pero no sustituye un pool en producción concurrente.

### Strategy

```txt
ProfileAnalyzer
├── BasicProfileStrategy
├── LanguageAnalysisStrategy
├── CollaborationAnalysisStrategy
└── RepositoryAnalysisStrategy
```

`InterfaceAnalysis` define el contrato. Cada estrategia tiene un nombre, recibe el mismo `UserProfile`, genera un resultado independiente y puede agregarse o reemplazarse sin modificar el orquestador. `github_router.py` selecciona e inyecta las estrategias.

### Adapter, Repository y Service Layer

* `GitHubAdapter` desacopla la API externa del modelo interno.
* Los repositories aíslan consultas SQL, aunque su adopción es parcial porque `DataRegister` también ejecuta SQL directamente.
* `ProfileAnalyzer` y el servicio de hashing encapsulan lógica fuera de las rutas.

---

## Base de datos

### Tablas

| Tabla              | Responsabilidad                            | Estado                                      |
| ------------------ | ------------------------------------------ | ------------------------------------------- |
| `users`            | Usuarios locales y hashes                  | Implementada y utilizada                    |
| `github_profiles`  | Datos principales de perfiles             | Implementada para escritura                 |
| `repositories`     | Repositorios del perfil                    | Implementada para escritura                 |
| `languages`        | Lenguajes agregados y porcentajes          | Implementada para escritura                 |
| `collaborators`    | Colaboradores agregados                    | Implementada para escritura                 |
| `search_history`   | Historial por usuario y perfil             | Preparada; no conectada al frontend          |
| `cache_entries`    | Snapshot JSON en MySQL                     | Escritura implementada; sin lectura          |
| `profile_metrics`  | Métricas resumidas                         | Implementada para escritura                 |

### Relaciones

```txt
users ──< search_history >── github_profiles
                               ├──< repositories
                               ├──< languages
                               ├──< collaborators
                               ├──< cache_entries
                               └── profile_metrics
```

Todas las relaciones tienen claves foráneas con `ON DELETE CASCADE` y `ON UPDATE CASCADE`. `profile_metrics` mantiene una relación uno a uno; lenguajes y colaboradores tienen restricciones únicas por perfil.

### Conexión del backend

```txt
mysql.connector.connect(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
)
```

### Flujo real de persistencia

Al consultar un perfil nuevo:

1. Se consulta GitHub y se analiza el resultado.
2. Se escribe `core/storage/cache/users_cache.json`.
3. Se abre una transacción MySQL.
4. Se actualiza el perfil y se reemplazan repositorios, lenguajes y colaboradores.
5. Se actualizan las métricas.
6. Se agrega un snapshot a `cache_entries`.
7. Se confirma la transacción.

Si MySQL falla, el endpoint puede continuar respondiendo gracias al caché JSON.

### Limitaciones

* MySQL es destino de escritura, no fuente de recuperación de perfiles.
* `total_commits` siempre se persiste en `0`; no existe análisis real de commits.
* `search_history` no recibe registros desde el flujo actual.
* Los repositories SQL especializados no están integrados plenamente con `DataRegister`.
* El SQL de inicialización se ejecuta normalmente solo al crear el volumen de MySQL por primera vez.

---

## Funcionalidades

### Implementado

* **Búsqueda:** `GET /github/user/{username}`, consumido por el dashboard.
* **Perfil público:** username, nombre, bio, avatar, URL, repositorios públicos, followers, following, fecha de creación, ubicación, compañía, blog y Twitter.
* **Repositorios:** total analizado, más destacado por estrellas, más bifurcado, últimos actualizados, lenguajes principales y tarjetas en el dashboard.
* **Lenguajes:** bytes, orden de uso, lenguaje principal, porcentajes y cantidad de repositorios. El detalle se consulta para los primeros siete repositorios devueltos.
* **Colaboradores:** contributors de los primeros siete repositorios, agregación por usuario, contribuciones, repositorios compartidos y comparación con el dueño.
* **Caché JSON:** primera fuente consultada, usernames en minúsculas y escritura temporal con reemplazo. No tiene expiración ni refresco.
* **Dashboard:** perfil, métricas rápidas, repositorios, actividad según fechas, lenguajes, colaboradores y origen GitHub/caché.
* **Autenticación:** registro y login contra MySQL mediante `POST /auth/register` y `POST /auth/login`; contraseñas con PBKDF2-HMAC-SHA256.
* **Historial visual:** almacenado en `localStorage` y separado por usuario local.

### Parcial o preparado

* MySQL persiste análisis para escritura, pero el dashboard no los lee desde allí.
* La tabla y el repository del historial SQL existen, pero no están conectados.
* `/profile` y `/metrics` contienen texto temporal.
* El login valida credenciales; la sesión posterior solo se representa en `localStorage`.
* La columna de commits existe, pero siempre vale cero.
* Hay repositories especializados, aunque el flujo principal usa SQL directo desde `DataRegister`.
* La landing contiene cifras demostrativas, como “48 repositorios” y “1.8k estrellas”; no representan al usuario consultado.

### Limitaciones conocidas

* No hay paginación ni `per_page`: normalmente se analiza solo la primera página de repositorios de GitHub.
* Lenguajes y contributors se consultan únicamente para los primeros siete repositorios.
* El caché no caduca ni ofrece un mecanismo de actualización forzada.
* El historial está en `localStorage`, no en MySQL.
* No existe una sesión JWT o de servidor.
* Las métricas de commits no están implementadas.

---

## Seguridad y configuración

### Implementado

* Los `.env` están ignorados por Git y no se detectaron archivos `.env` versionados.
* `core/.env.example` no contiene un token real.
* El token de GitHub se envía mediante el header de autorización.
* Las contraseñas usan PBKDF2-HMAC-SHA256, salt aleatorio de 16 bytes, 600.000 iteraciones y comparación constante con `hmac.compare_digest`.
* Las consultas SQL usan parámetros para reducir el riesgo de inyección.
* Los errores de base de datos no exponen credenciales.
* El username incluido en URLs se codifica con `encodeURIComponent`.
* CORS restringe los orígenes a `localhost` en los puertos 5173 y 5174.

### Pendiente o limitado

* No hay JWT, cookie de sesión ni token propio de autenticación.
* Las rutas del dashboard solo comprueban `localStorage`.
* Los endpoints de análisis no exigen autenticación.
* No hay cierre de sesión visible, complejidad mínima de contraseña ni rate limiting propio.
* La validación del username es básica.
* No hay CSRF; tampoco se usan cookies autenticadas actualmente.
* No existen políticas de expiración de caché.
* Las credenciales predeterminadas de MySQL son `root/root` y `MYSQL_ROOT_PASSWORD` figura directamente en Compose.
* El backend usa `--reload` y no distingue configuración de desarrollo y producción.
* No se observan tests de seguridad ni pruebas automatizadas.

### Archivos que no deberían subirse

* `core/.env` y `ui/.env`.
* Tokens de GitHub y contraseñas reales de MySQL.
* `core/storage/cache/*.json`.
* `node_modules/`, `ui/dist/`, logs y archivos temporales.
* Claves privadas, certificados o backups de base de datos.

Las reglas actuales de `.gitignore` cubren los `.env`, el caché JSON, dependencias, builds y logs.

---

## Estructura de carpetas

```txt
MyGit/
├── core/
│   ├── .env.example
│   └── app/
│       ├── adapters/
│       ├── config/
│       ├── infrastructure/
│       ├── persistence/
│       ├── repositories/
│       ├── routers/
│       ├── schemas/
│       ├── services/
│       ├── strategies/
│       ├── DockerFile
│       └── main.py
├── db/
│   └── MyGitDB.sql
├── ui/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── css/
│   │   ├── router/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── viewModels/
│   │   └── views/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
├── docker-compose.yml
├── README.md
└── doc.md
```

| Carpeta         | Responsabilidad                                      |
| --------------- | ---------------------------------------------------- |
| `core`          | Backend y lógica del sistema                         |
| `db`            | Definición inicial de MySQL                          |
| `ui`            | Aplicación Vue                                       |
| `adapters`      | Integración externa con GitHub                       |
| `routers`       | Interfaz HTTP                                        |
| `strategies`    | Algoritmos intercambiables de análisis               |
| `services`      | Orquestación y lógica transversal                    |
| `repositories`  | Acceso SQL especializado                             |
| `persistence`   | Caché y registro de resultados                       |
| `infrastructure`| Conexión y configuración técnica                     |
| `schemas`       | Modelos internos                                     |
| `views`         | Páginas del frontend                                 |
| `viewModels`    | Estado y lógica de presentación                      |
| `components`    | Piezas visuales reutilizables                        |

Los services del frontend se ocupan de la comunicación HTTP y del almacenamiento local.

---

## Endpoints

| Método | Endpoint                                  | Estado o descripción     |
| ------ | ----------------------------------------- | ------------------------ |
| GET    | `/`                                       | Prueba básica            |
| GET    | `/db/health`                              | Health check MySQL       |
| POST   | `/auth/register`                          | Funcional                |
| POST   | `/auth/login`                             | Funcional                |
| GET    | `/github/user/{username}`                 | Flujo principal          |
| GET    | `/github/user/{username}/repositories`    | Funcional                |
| GET    | `/github/user/{username}/languages`       | Funcional                |
| GET    | `/github/user/{username}/contributors`    | Funcional                |
| GET    | `/docs`                                   | Swagger automático       |
| GET    | `/openapi.json`                           | Esquema OpenAPI          |

---

## Comandos útiles

### Variables del backend

```bash
Copy-Item core\.env.example core\.env
```

Luego puede completarse `GITHUB_TOKEN` para disponer de una cuota mayor de la API.

### Docker

```bash
docker compose up -d --build
```

```bash
docker compose ps
```

```bash
docker compose logs -f backend
```

```bash
docker compose down
```

El siguiente comando también elimina los datos locales de MySQL:

```bash
docker compose down -v
```

> **Advertencia:** `docker compose down -v` es destructivo para la base local.

### Backend local

Desde `core/app`:

```bash
python -m venv .venv
```

```bash
.\.venv\Scripts\Activate.ps1
```

```bash
python -m pip install -r config/requirements.txt
```

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Fuera de Docker, `DB_HOST` normalmente debe ser `localhost`, no `database`.

### Frontend

```bash
cd ui
```

```bash
npm install
```

Para reproducir exactamente el lockfile:

```bash
npm ci
```

```bash
npm run dev
```

```bash
npm run build
```

```bash
npm run preview
```

Configuración de `ui/.env`:

```env
VITE_API_URL=http://localhost:8000
```

### Health checks

```bash
Invoke-RestMethod http://localhost:8000/
```

```bash
Invoke-RestMethod http://localhost:8000/db/health
```

Swagger está disponible en `http://localhost:8000/docs`.

### Base de datos

```bash
docker compose exec database mysql -uroot -proot MyGitDB
```

```sql
SHOW TABLES;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM github_profiles;
SELECT COUNT(*) FROM repositories;
```

---

Esta documentación complementa el README principal, que queda enfocado en presentación e instalación rápida.
