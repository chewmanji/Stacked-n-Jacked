from fastapi import APIRouter, Depends, HTTPException, Path, Query
from core.dependencies import get_db
from core import schemas, crud
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/exercises", tags=["Exercise"])


@router.get("")
async def get_exercises(skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 50,
                        db: Session = Depends(get_db)) -> list[schemas.Exercise]:
    return crud.get_exercises(db, skip=skip, limit=limit)


@router.get("/{exercise_id}")
async def get_exercise(exercise_id: Annotated[int, Path(title="Exercise ID to get", gt=0)],
                       db: Session = Depends(get_db)) -> schemas.Exercise:
    exercise = crud.get_exercise_by_id(db, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise
