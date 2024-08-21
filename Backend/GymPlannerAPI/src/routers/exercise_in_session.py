# from fastapi import APIRouter, Depends, HTTPException, status
# from typing import Annotated
# from sqlalchemy.orm import Session
#
# import src.crud.exercise_in_session as exercise_in_session_service
# import src.crud.user_exercise as user_exercise_service
# from src.schemas.user import User
# from src.schemas.workout_exercise import ExerciseInSessionBase, ExerciseInSession
# from src.core.dependencies import get_db, get_current_user
#
# router = APIRouter(prefix="/exercises_in_session", tags=["Exercise in session"])
#
#
# @router.post("", status_code=status.HTTP_201_CREATED, response_model=ExerciseInSession)
# def create_exercise_in_session(current_user: Annotated[User, Depends(get_current_user)],
#                                ex_session_base: ExerciseInSessionBase,
#                                db: Session = Depends(get_db)):
#     user_exercises = user_exercise_service.get_user_exercises_by_user_id(db, current_user.id)
#
#     if not (ex_session_base.user_exercise_id in [user_exercise.id for user_exercise in user_exercises]):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You do not have access to a exercise that you try to assign exercise in session to."
#         )
#
#     return exercise_in_session_service.create_exercise_in_session(db, ex_session_base)
#
#
# @router.get("/{exercise_in_session_id}", status_code=status.HTTP_200_OK, response_model=ExerciseInSession)
# def get_exercise_in_session_by_id(exercise_in_session_id: int, current_user: Annotated[User, Depends(get_current_user)],
#                                   db: Session = Depends(get_db)):
#     exercise_in_session = exercise_in_session_service.get_exercise_in_session_by_id(db, exercise_in_session_id)
#     if not exercise_in_session:
#         raise HTTPException(status_code=404, detail="Exercise in session not found")
#
#     if not exercise_in_session.user_exercise.user_id == current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You do not have access to a exercise in session that you try to get."
#         )
#
#     return exercise_in_session
