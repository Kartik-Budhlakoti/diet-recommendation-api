# Diet Recommendation API

A backend API for personalized diet recommendations built with FastAPI and PostgreSQL. It calculates BMI and daily calorie requirements using the Harris-Benedict equation and returns structured meal plans based on the user's health goal.

Built as a college assignment and used as a learning ground for backend architecture, containerization, and CI/CD — before scaling into a larger healthcare security project.

**Live API:** https://diet-recommendation-api-pk9g.onrender.com  
**Interactive Docs:** https://diet-recommendation-api-pk9g.onrender.com/docs  
**GitHub:** https://github.com/Kartik-Budhlakoti/diet-recommendation-api

---

## What It Does

- Accepts a user's health profile — age, weight, height, gender, activity level, health goal
- Calculates BMI and classifies it (underweight, normal, overweight, obese)
- Predicts daily calorie requirement using the Harris-Benedict BMR formula with activity multipliers
- Returns a structured meal plan across 5 diet categories — weight loss, weight gain, muscle building, balanced, diabetes management
- Logs food items against a user profile with optional macro tracking

The recommendation engine is rule-based by design. The original synopsis called for a Random Forest model but there was no real training dataset available. Deploying a model that cannot be explained or verified is worse engineering than an honest rule-based system that works correctly and can be fully justified — so the ML approach was dropped in favour of this.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | PostgreSQL (via SQLAlchemy ORM) |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## Project Structure

```
diet-recommendation-api/
├── app/
│   ├── main.py           # App instance, CORS middleware, router registration
│   ├── database.py       # SQLAlchemy engine, session factory, Base
│   ├── models.py         # Database table definitions — User, FoodLog
│   ├── schemas.py        # Pydantic schemas — input validation and response shaping
│   └── routers/
│       ├── users.py      # User registration
│       ├── diet.py       # BMI, BMR calculation and meal plan engine
│       └── logs.py       # Food logging and retrieval
├── .github/
│   └── workflows/
│       └── deploy.yml    # CI/CD pipeline — build and deploy on every push
├── .env                  # Environment variables (never pushed to GitHub)
├── .gitignore
├── docker-compose.yml    # API + PostgreSQL orchestration for local development
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Getting Started

### Option 1 — Docker Compose (Recommended)

This spins up the API and PostgreSQL together with one command. No manual database setup needed.

```bash
git clone https://github.com/Kartik-Budhlakoti/diet-recommendation-api.git
cd diet-recommendation-api
```

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://dietuser:dietpassword@db:5432/dietdb
POSTGRES_DB=dietdb
POSTGRES_USER=dietuser
POSTGRES_PASSWORD=dietpassword
```

Then run:

```bash
docker compose up --build
```

API available at `http://127.0.0.1:8000`  
Docs at `http://127.0.0.1:8000/docs`

---

### Option 2 — Local Python Setup

```bash
git clone https://github.com/Kartik-Budhlakoti/diet-recommendation-api.git
cd diet-recommendation-api

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
DATABASE_URL=sqlite:///./diet_app.db
```

Run the server:

```bash
uvicorn app.main:app --reload
```

---

## API Reference

### Base URL

```
http://127.0.0.1:8000/api/v1              # local
https://diet-recommendation-api-pk9g.onrender.com/api/v1   # production
```

---

### Register a User

```
POST /api/v1/users/register
```

**Request Body:**

```json
{
  "name": "Kartik",
  "age": 21,
  "weight_kg": 70.0,
  "height_cm": 175.0,
  "gender": "male",
  "activity_level": "moderate",
  "health_goal": "muscle_building"
}
```

**Allowed values:**

| Field | Allowed Values |
|-------|---------------|
| gender | `male`, `female` |
| activity_level | `sedentary`, `light`, `moderate`, `active`, `very_active` |
| health_goal | `weight_loss`, `weight_gain`, `muscle_building`, `balanced`, `diabetes` |

**Response `200 OK`:**

```json
{
  "id": 1,
  "name": "Kartik",
  "age": 21,
  "weight_kg": 70.0,
  "height_cm": 175.0,
  "gender": "male",
  "activity_level": "moderate",
  "health_goal": "muscle_building",
  "created_at": "2026-01-15T10:30:00Z"
}
```

> The `id` returned here is the `user_id` required for all subsequent requests. Save it after registration.

> **Note on authentication:** This prototype uses a simple user_id based flow — no passwords, no tokens. JWT authentication with proper session management is planned for the next version. The architecture already supports adding it with minimal changes — an auth router and middleware layer is all that's needed.

---

### Get Diet Recommendation

```
GET /api/v1/diet/{user_id}
```

**Response `200 OK`:**

```json
{
  "user_id": 1,
  "bmi": 22.86,
  "bmi_category": "normal",
  "daily_calorie": 2734.45,
  "diet_category": "muscle_building",
  "breakfast": "6 egg whites + 1 whole egg omelette, oats (complex carbs for pre-workout energy), black coffee",
  "lunch": "Grilled chicken breast, brown rice (complex carbs - chawal with husk), steamed broccoli",
  "dinner": "Paneer or chicken, sauteed vegetables, small portion of sweet potato (shakarkand)",
  "snacks": "Whey protein shake post-workout, handful of almonds, fish oil (omega-3) + multivitamin tablet",
  "protein_g": 180.0,
  "carbs_g": 200.0,
  "fat_g": 50.0
}
```

**BMI Categories:**

| BMI Range | Category |
|-----------|----------|
| Below 18.5 | underweight |
| 18.5 – 24.9 | normal |
| 25 – 29.9 | overweight |
| 30 and above | obese |

**Error `404`** — returned when user_id does not exist.

---

### Log Food

```
POST /api/v1/logs/
```

**Request Body:**

```json
{
  "user_id": 1,
  "food_item": "Brown rice",
  "calories": 215.0,
  "protein_g": 4.5,
  "carbs_g": 45.0,
  "fat_g": 1.8
}
```

`protein_g`, `carbs_g`, `fat_g` are optional. Only `user_id`, `food_item`, and `calories` are required.

---

### Get Food Logs

```
GET /api/v1/logs/{user_id}
```

Returns all food entries logged by that user as a JSON array.

---

## CI/CD Pipeline

Every push to the `main` branch automatically triggers the GitHub Actions pipeline:

1. Checks out the code on a fresh Ubuntu runner
2. Builds the Docker image — if this fails, deployment stops
3. Sends a deploy signal to Render via a secured webhook

The deploy hook URL is stored as a GitHub repository secret and never appears in code or logs. If the Docker build fails for any reason, Render never receives the signal and the broken code never reaches production.

Pipeline status is visible on the GitHub Actions tab of this repository.

---

## Docker

### Run with Docker Compose (API + PostgreSQL)

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

### Run with Docker only

```bash
docker build -t diet-api .
docker run -p 8000:8000 -e DATABASE_URL=sqlite:///./diet_app.db diet-api
```

---

## Deployment

Deployed on Render with a managed PostgreSQL database.

**Live URL:** https://diet-recommendation-api-pk9g.onrender.com  
**Docs:** https://diet-recommendation-api-pk9g.onrender.com/docs

> Render free tier spins down after 15 minutes of inactivity. The first request after that takes 20-30 seconds to wake up. Hit the live URL once before testing if you haven't used it recently.

### Deploy Your Own Instance

1. Fork this repository
2. Create a **Web Service** on Render and connect your fork
3. Create a **PostgreSQL** database on Render (free tier)
4. Set environment variable on the web service:
   - `DATABASE_URL` — use the Internal Database URL from your Render PostgreSQL instance
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. For CI/CD — add your Render deploy hook URL as a GitHub secret named `RENDER_DEPLOY_HOOK`

---

## Roadmap

This project is the starting point. The architecture decisions made here — separation of concerns, environment-based configuration, containerized deployment, automated CI/CD — are intentional foundations for what comes next.

### v1.0 — Current
- [x] User registration and health profile
- [x] BMI and BMR calculation (Harris-Benedict equation)
- [x] Rule-based diet recommendation engine across 5 categories
- [x] Food logging and retrieval
- [x] PostgreSQL via Docker Compose for local development
- [x] PostgreSQL on Render for production
- [x] Dockerized with health check orchestration
- [x] GitHub Actions CI/CD pipeline

### What comes next
A separate project is currently in development — a medical data integrity verification system focused on cryptographic tamper detection for healthcare files, DevSecOps pipeline integration, and role-based access control aligned with healthcare data security principles. This diet API served as the architectural foundation and learning ground for that work.

---

## Author

**Kartik Budhlakoti**  
B.Tech Computer Science — 3rd Year  
Learning path: Python → Linux → Docker → FastAPI → DevOps → DevSecOps  
GitHub: https://github.com/Kartik-Budhlakoti