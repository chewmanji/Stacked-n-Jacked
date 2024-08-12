from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import engine
from src.core import models
from src.routers import user, exercise_in_session
from src.routers import plan, exercise, user_exercise, training, training_session
import uvicorn


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(user_exercise.router)
app.include_router(training.router)
app.include_router(plan.router)
app.include_router(training_session.router)
app.include_router(exercise_in_session.router)

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return "Hello wurld"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)





