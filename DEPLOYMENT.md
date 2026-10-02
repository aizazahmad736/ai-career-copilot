# Deployment Guide

## 1. Deploy the API and database on Render

1. Push the repository to a Git provider and create a Render Blueprint from the repository root. Render reads `render.yaml` to provision the PostgreSQL database and FastAPI service.
2. Set `GEMINI_API_KEY` in the Render service if you want Gemini-powered resume/interview analysis. Without it, the app uses clearly labelled heuristic fallbacks.
3. After creating the Vercel project, replace the `CORS_ORIGINS` placeholder with a JSON array containing the exact frontend origin, for example `["https://your-project.vercel.app"]`.
4. Confirm `AUTH_REQUIRED=true` and that Render generated a unique `AUTH_SECRET`. The API refuses to start with the local development secret when hosted auth is enabled.

## 2. Deploy the frontend on Vercel

1. Import the repository into Vercel and set the project root to `frontend`.
2. Add `VITE_API_BASE_URL` as `https://<your-render-service>.onrender.com/api/v1`.
3. Deploy, then set the exact assigned Vercel origin in Render's `CORS_ORIGINS` environment variable and redeploy the API.
4. Open the Vercel URL, create an account, upload a test resume, and verify analysis, dashboard, learning-plan progress, interview practice, and application tracking.

## Environment variables

Backend variables are documented in `backend/.env.example`. Hosted configuration must set:

- `DATABASE_URL`: Render's private PostgreSQL connection string.
- `AUTH_REQUIRED=true` and a unique `AUTH_SECRET` of at least 32 characters.
- `CORS_ORIGINS`: a JSON array containing the Vercel origin, with no wildcard.
- `GEMINI_API_KEY`: optional, but required for full Gemini-backed analysis and interview evaluation.

The frontend variable is documented in `frontend/.env.example`. Never put backend secrets in a `VITE_` variable; Vite embeds those values in browser assets.

## Operational notes

- The API stores resume text, extracted profile data, interview answers, and job/application history in PostgreSQL. Limit database access, enable provider backups, and define retention/deletion policies before accepting real candidate data.
- Browser-provided Gemini, Tavily, and Serper keys remain in browser local storage and are sent to the API only for the relevant request. Use HTTPS in production.
- Render/Vercel accounts, a Git remote, production domains, and provider credentials are not available in this workspace, so this repository is deployment-prepared but not publicly deployed.