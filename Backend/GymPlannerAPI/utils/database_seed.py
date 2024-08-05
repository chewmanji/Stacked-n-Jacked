import os
import sys
import pandas as pd
from core.models import Exercise
from core.database import SessionLocal
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from youtube_utils import get_youtube_video_url

load_dotenv()
YT_API_KEY = os.getenv('YOUTUBE_API_KEY')
DATASET_PATH = os.getenv('DATASET_PATH')

db: Session = SessionLocal()


def seed_exercises(filepath):
    exercises = pd.read_excel(filepath, sheet_name=None)
    existing_exercise_names = set(name for (name,) in db.query(Exercise.name).all())
    for sheet_name, sheet in exercises.items():
        sheet = sheet.drop_duplicates(subset=['Exercise_Name'])

        for name, target_muscle, equipment in zip(sheet['Exercise_Name'], sheet['muscle_gp'], sheet['Equipment']):
            equipment = equipment if type(equipment) is not float else None  # nan values to None so NULL is in DB
            ex = Exercise(name=name, target_muscle=target_muscle, equipment=equipment)
            if ex.name not in existing_exercise_names:
                db.add(ex)
                db.commit()


def update_exercises_url():
    ex_to_update = db.query(Exercise).filter(Exercise.youtube_url == None)
    for ex in ex_to_update:
        if ex.youtube_url is None:
            try:
                ex.youtube_url = get_youtube_video_url(f"{ex.name} exercise tutorial", YT_API_KEY)
                db.commit()
            except Exception as e:
                print("Quotas exceeded for today! Exiting...")
                print(f"Error: {e}")
                sys.exit(1)


if __name__ == "__main__":
    # seed_exercises(DATASET_PATH)
    update_exercises_url()

db.close()
