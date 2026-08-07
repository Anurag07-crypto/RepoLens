# Deploying RepoLens to Render

This repository is arranged so Render can deploy both backend and frontend as separate services.

Recommended settings (Render dashboard):

Backend (Web Service)
- Root Directory: `RepoLens`
- Environment: `Python`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn Backend.server:app --host 0.0.0.0 --port $PORT`
- Health check path: `/docs`
- Environment variables:
  - `GROQ_API_KEY` (secret)
  - `CORS_ALLOWED_ORIGINS` (e.g. `https://<frontend>.onrender.com`)
  - `UVICORN_RELOAD=false`

Frontend (Static Site)
- Root Directory: `FRONTEND`
- Environment: `Static`
- Build Command: `npm ci && npm run build`
- Publish Directory: `dist`
- Build env var (set in Render): `VITE_API_URL` = `https://<backend>.onrender.com`

Optional: Use `render.yaml` (already present) for IaC. Replace placeholder domain values before using.
