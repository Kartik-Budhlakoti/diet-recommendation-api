from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users, diet, logs

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Diet Recommendation System",
    description="Backend API for personalized diet recommendations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(diet.router, prefix="/api/v1/diet", tags=["Diet"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["Logs"])

@app.get("/")
def root():
    return {"message": "Diet API is running"}