# HirePath Backend

Backend Django + Django REST Framework para TalentPilot AI / HirePath.

## Ejecutar localmente

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

La API queda disponible en `http://127.0.0.1:8000/api/`.

## Autenticacion

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/me/`

El frontend Next.js debe enviar `Authorization: Bearer <access_token>` en endpoints privados.

## Perfil y datos profesionales

- `GET|PUT /api/profile/`
- `GET|POST /api/educations/`
- `GET|POST /api/work-experiences/`
- `GET|POST /api/projects/`
- `GET|POST /api/certifications/`
- `GET|POST /api/user-skills/`

## Vacantes y workflows

- `GET|POST /api/job-postings/`
- `GET|POST /api/job-search-criteria/`
- `POST /api/jobs/{id}/analyze-match/`
- `POST /api/jobs/{id}/recommend-salary/`
- `POST /api/jobs/{id}/generate-cv/`

## Postulaciones

- `GET|POST /api/applications/`
- `GET|PUT|PATCH /api/applications/{id}/`
- `POST /api/applications/{id}/generate-answers/`
- `POST /api/applications/{id}/mark-applied/`
- `POST /api/applications/{id}/generate-interview-prep/`

## PostgreSQL

Copia `.env.example` a `.env` y cambia:

```env
DB_ENGINE=postgres
POSTGRES_DB=hirepath
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
