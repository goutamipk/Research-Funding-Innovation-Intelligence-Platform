# Research Funding & Innovation Intelligence Platform

Production-ready web application and FastAPI backend for AI-powered research funding recommendations.

---

## 🚀 FastAPI Backend

The backend is built with **Python 3.12**, **FastAPI**, **Uvicorn**, and **Scikit-Learn** using a modular architecture with structured logging, Pydantic v2 schemas, global exception handling, and RESTful API versioning (`/api/v1`).

### 📁 Project Architecture

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── health.py          # System health & probes (/health, /health/readiness)
│   │       │   ├── recommendations.py # AI funding recommendations (/recommendations/predict)
│   │       │   └── grants.py          # Grant search & detail endpoints (/grants)
│   │       └── router.py              # Main API v1 router
│   ├── core/
│   │   ├── config.py                  # Pydantic BaseSettings environment config
│   │   ├── logger.py                  # Structured colored logging setup
│   │   ├── middleware.py              # CORS & process time header middleware
│   │   └── exceptions.py              # Global exception handlers & custom errors
│   ├── services/
│   │   ├── recommendation_service.py # Recommendation orchestrator
│   │   └── grant_service.py          # Grants search & filtering service
│   ├── ml/
│   │   └── recommender.py             # TF-IDF & Cosine Similarity ML engine
│   ├── datasets/
│   │   └── loader.py                  # CSV grant dataset loader with fallback
│   ├── models/
│   │   └── schemas.py                 # Request and response Pydantic schemas
│   └── utils/
│       └── text_processing.py         # Text cleaning and similarity helper functions
│
├── main.py                            # FastAPI entry point with async lifespan handler
├── config.py                          # Root settings alias
├── logger.py                          # Root logger alias
├── requirements.txt                   # Production Python dependencies
├── .env                               # Active environment file
├── .env.example                       # Environment template
└── README.md                          # Documentation
```

---

## 🛠️ Prerequisites & Setup

- **Python 3.12** or higher
- `pip` or `uv`

### 1. Create Virtual Environment

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env` if not already present:

```bash
cp .env.example .env
```

Environment options:
- `PROJECT_NAME`: Title shown in Swagger UI.
- `BACKEND_CORS_ORIGINS`: Allowed origins for React frontend (e.g. `["http://localhost:5173"]`).
- `DATASET_PATH`: Path to research dataset CSV.
- `LOG_LEVEL`: Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

---

## 💻 Running the Backend Server

Start the Uvicorn server:

```bash
python main.py
```

Or using `uvicorn` directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will initialize the dataset and ML model during startup (`lifespan` handler).

---

## 📡 API Endpoints & Interactive Documentation

Once the server is running, explore the interactive documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema**: [http://127.0.0.1:8000/api/v1/openapi.json](http://127.0.0.1:8000/api/v1/openapi.json)

### Key Endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System health check, environment, and dataset index count |
| `GET` | `/api/v1/health/liveness` | Liveness probe for containers |
| `GET` | `/api/v1/health/readiness` | Readiness probe for ML model readiness |
| `POST` | `/api/v1/recommendations/predict` | Generate AI grant recommendations from proposal abstract |
| `GET` | `/api/v1/grants` | List & search grants with pagination and filters |
| `GET` | `/api/v1/grants/{grant_id}` | Retrieve grant details by ID |

---

## 🧪 Request Example

**POST** `/api/v1/recommendations/predict`

```json
{
  "abstract": "We propose developing a deep learning transformer architecture for early-stage climate risk assessment and flood prediction.",
  "topics": ["AI", "Climate Science", "Deep Learning", "Environmental Engineering"],
  "min_budget": 100000,
  "max_budget": 1000000,
  "top_k": 3
}
```

**Response**:

```json
{
  "success": true,
  "total": 3,
  "processing_time_ms": 12.45,
  "query_topics": ["AI", "Climate Science", "Deep Learning", "Environmental Engineering"],
  "recommendations": [
    {
      "grant": {
        "id": "GRANT-2024-CLIMATE-02",
        "title": "Climate Resilience & Earth Observation Analytics",
        "agency": "NASA Earth Science Division",
        "description": "Research proposals leveraging satellite imagery, machine learning...",
        "budget": 500000.0,
        "startDate": "2024-02-01",
        "endDate": "2024-11-30",
        "topics": ["Climate Science", "Remote Sensing", "Environmental Engineering"],
        "url": "https://nasa.gov/earth/climate-analytics-grant"
      },
      "score": 0.8412,
      "confidence": "High",
      "matched_keywords": ["climate", "learning", "prediction"]
    }
  ]
}
```

---

## 🎨 React Frontend Setup

```bash
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`.
