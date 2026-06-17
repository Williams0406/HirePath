# HirePath Frontend

Frontend Next.js con App Router para HirePath.

## Ejecutar

```powershell
npm install
npm run dev
```

La app usa por defecto:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8010/api
```

## Rutas

- `/`
- `/login`
- `/register`
- `/admin`

El panel `/admin` requiere sesion activa y muestra informacion del usuario autenticado.
