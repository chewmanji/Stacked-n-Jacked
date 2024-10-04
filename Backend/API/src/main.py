from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from src.core.database import Base, engine
from src.routers import (
    user,
    exercise,
    workout_exercise,
    workout,
    set
)

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(workout_exercise.router)
app.include_router(workout.router)
app.include_router(set.router)


origins = ["http://localhost:3000", "https://stacked-n-jacked.wojtek.s.solvro.pl"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*.wojtek.s.solvro.pl", "localhost"])


@app.get("/")
async def main():
    return "Hello wurld"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
