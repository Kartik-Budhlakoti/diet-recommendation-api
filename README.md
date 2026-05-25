# 🥗 Diet Recommendation API

A production-ready REST API for personalized diet recommendations based on BMI analysis, BMR calculation, and health goal-based meal planning.

Built with **FastAPI + SQLAlchemy + SQLite + Docker** as the backend foundation for an AI-powered diet recommendation system.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Docker](#docker)
- [Deployment](#deployment)
- [Roadmap](#roadmap)

---

## Overview

This API handles:
- User registration with health profile (age, weight, height, activity level, health goal)
- Automatic BMI calculation and classification
- Daily calorie requirement prediction using the Harris-Benedict BMR formula
- Rule-based personalized meal plan generation across 5 diet categories
- Real-time food logging and retrieval per user

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | SQLite (via SQLAlchemy ORM) |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Container | Docker |
| Deployment | Render |

---

## Project Structure

```
diet-recommendation-api/
├── app/
│   ├── main.py          # FastAPI app instance, middleware, router registration
│   ├── database.py      # SQLAlchemy engine, session, base configuration
│   ├── models.py        # Database table definitions (User, FoodLog)
│   ├── schemas.py       # Pydantic schemas for request/response validation
│   └── routers/
│       ├── users.py     # User registration endpoint
│       ├── diet.py      # Diet recommendation engine
│       └── logs.py      # Food logging endpoints
├── .env                 # Environment variables (never pushed to GitHub)
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker (optional)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Kartik-Budhlakoti/diet-recommendation-api.git
cd diet-recommendation-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=sqlite:///./diet_app.db" > .env

# Run the server
uvicorn app.main:app --reload
```

API will be available at `http://127.0.0.1:8000`

Interactive docs at `http://127.0.0.1:8000/docs`

---

## API Reference

### Base URL
```
http://127.0.0.1:8000/api/v1        # local
https://diet-recommendation-api-pk9g.onrender.com/api/v1    # production
```

---

### Users

#### Register a User
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
  "created_at": "2026-01-15T10:30:00"
}
```

> ⚠️ **Important for Frontend:** Save the returned `id` — this is the `user_id` required for all subsequent requests. There is no login system in this prototype. The frontend should store this value in local state or localStorage after registration.

---

### Diet Recommendations

#### Get Personalized Diet Recommendation
```
GET /api/v1/diet/{user_id}
```

**Path Parameter:**
| Parameter | Type | Description |
|-----------|------|-------------|
| user_id | integer | ID returned from registration |

**Response `200 OK`:**
```json
{
  "user_id": 1,
  "bmi": 22.86,
  "bmi_category": "normal",
  "daily_calories": 2734.45,
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

**Error `404`:**
```json
{
  "detail": "User not found"
}
```

---

### Food Logs

#### Log a Food Item
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

> `protein_g`, `carbs_g`, `fat_g` are optional. Only `user_id`, `food_item`, and `calories` are required.

**Response `200 OK`:**
```json
{
  "id": 1,
  "user_id": 1,
  "food_item": "Brown rice",
  "calories": 215.0,
  "protein_g": 4.5,
  "carbs_g": 45.0,
  "fat_g": 1.8,
  "logged_at": "2026-01-15T13:45:00"
}
```

#### Get All Food Logs for a User
```
GET /api/v1/logs/{user_id}
```

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "food_item": "Brown rice",
    "calories": 215.0,
    "protein_g": 4.5,
    "carbs_g": 45.0,
    "fat_g": 1.8,
    "logged_at": "2026-01-15T13:45:00"
  },
  {
    "id": 2,
    "user_id": 1,
    "food_item": "Grilled chicken",
    "calories": 165.0,
    "protein_g": 31.0,
    "carbs_g": 0.0,
    "fat_g": 3.6,
    "logged_at": "2026-01-15T14:20:00"
  }
]
```

## Docker

### Build
```bash
docker build -t diet-api .
```

### Run
```bash
docker run -p 8000:8000 diet-api
```

### With Environment Variable
```bash
docker run -p 8000:8000 -e DATABASE_URL=sqlite:///./diet_app.db diet-api
```

---

## Deployment

This API is deployed on **Render** (free tier).

**Live URL:** `https://diet-recommendation-api-pk9g.onrender.com/`

**Interactive Docs:** `https://diet-recommendation-api-pk9g.onrender.com/docs`

### Deploy Your Own Instance

1. Fork this repository
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repository
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable:
   - `DATABASE_URL` = `sqlite:///./diet_app.db`
6. Deploy

---

## Roadmap

This prototype is the foundation of a larger healthcare backend system currently in development.

### v1.0 — Current (Prototype)
- [x] User registration and health profile
- [x] BMI and BMR calculation
- [x] Rule-based diet recommendation engine
- [x] Food logging and retrieval
- [x] Dockerized deployment
---

## Author

**Kartik Budhlakoti**  
B.Tech Computer Science — 3rd Year  
Currently learning: Linux, Docker, FastAPI  
GitHub: github.com/Kartik-Budhlakoti