from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import Annotated
from sqlalchemy.orm import Session

import src.crud.exercise as exercise_service
from src.schemas.exercise import Exercise
from src.core.dependencies import get_db

router = APIRouter(prefix="/exercises", tags=["Exercise"])


@router.get("", response_model=list[Exercise])
async def get_exercises(skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 50,
                        db: Session = Depends(get_db)):
    return exercise_service.get_exercises(db, skip=skip, limit=limit)


@router.get("/{exercise_id}", response_model=Exercise)
async def get_exercise(exercise_id: Annotated[int, Path(title="Exercise ID to get", gt=0)],
                       db: Session = Depends(get_db)):
    exercise = exercise_service.get_exercise_by_id(db, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise
