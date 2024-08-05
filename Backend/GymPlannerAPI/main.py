from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine
from core import models
from routers import user, exercise, user_exercise, training
import uvicorn


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(user_exercise.router)
app.include_router(training.router)

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





