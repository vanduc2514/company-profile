# InsightEngine — Automated Enterprise Customer Profile Creation

[![Continuous Integration](https://github.com/nvduc/insightengine-profile-app/actions/workflows/ci.yml/badge.svg)](https://github.com/nvduc/insightengine-profile-app/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

InsightEngine replaces manual, fragmented data gathering for enterprise customer profiles with an automated AI assembly line.

---

## 🌟 Features

- **Multi-Source Ingestion**: Input raw snippets from Google Search, LinkedIn, company websites, and business registration portals.
- **AI Processing Pipeline**: Animated stepper simulating data collection, NLP analysis, schema structuring, and confidence scoring.
- **Structured Enterprise Profile**:
  - Company overview & scale classification (Startup, SME, Large Enterprise)
  - Industry taxonomy & market coverage
  - Key products/services extraction
  - Registration details & verification status
  - Competitor, regulatory risk, and growth metrics
  - Real-time intelligence feed
- **Persistence & Export**: Automatic local/Firestore storage, real-time search, and 1-click JSON export.

---

## 🛠️ Stack Architecture

- **Frontend**: Single Page Application (SPA) built with Semantic HTML5, Vanilla ES6+ JS, and Custom CSS Tokens (matching Stitch design).
- **Backend**: FastAPI (Python 3.12) containerized with Docker and deployed to **Google Cloud Run**.
- **Database**: Google Firestore (with local in-memory fallback).
- **CI/CD**: GitHub Actions workflows for automated testing, container registry push, Cloud Run deployment, and Firebase Hosting.

---

## 🚀 Local Quickstart

### 1. Run Frontend Locally

Open `frontend/index.html` directly in any standard browser, or serve via Python static server:

```bash
cd frontend
python3 -m http.server 8000
```

Navigate to `http://localhost:8000`.

### 2. Run Backend API Locally

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

API docs will be available at `http://localhost:8080/docs`.

### 3. Run Backend Unit Tests

```bash
cd backend
pytest -v
```

---

## ☁️ Google Cloud Deployment

1. **Deploy to Cloud Run via CLI**:
   ```bash
   gcloud run deploy insightengine-backend \
     --source ./backend \
     --region us-central1 \
     --allow-unauthenticated
   ```

2. **GitHub Actions Secrets Required**:
   - `GCP_PROJECT_ID`: Your Google Cloud Project ID
   - `GCP_SA_KEY`: Service Account JSON Key with Cloud Run Admin & Artifact Registry Writer roles
   - `FIREBASE_SERVICE_ACCOUNT`: Firebase Deployment Service Account JSON
