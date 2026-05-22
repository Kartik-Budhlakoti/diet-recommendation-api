from fastapi import FastAPI
from app.database import Base, engine
from app.routers import diet , users , logs
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Diet Recommendation API",
    description="Backend for personalized diet recommendation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(diet.router, prefix="/api/v1/diet", tags=["diet"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])

@app.get("/")
def root():
    return {"message": "Diet API is running"}