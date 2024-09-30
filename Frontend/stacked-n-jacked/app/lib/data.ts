import { Exercise, Workout } from "@/app/lib/definitions";
import { getToken } from "../actions/auth";

export async function fetchExercises(): Promise<Exercise[]> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises?limit=1000`
  );

  const data = await response.json();
  return data.map((ex) => mapExerciseToCamelCase(ex));
}

export async function fetchExerciseDetails(id: number): Promise<Exercise> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises/${id}`
  );

  const data = await response.json();
  return mapExerciseToCamelCase(data);
}

export async function fetchWorkouts(): Promise<Workout[]> {
  const token = await getToken();
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/workouts`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();
  return data.map((w) => mapWorkoutToCamelCase(w));
}

function mapExerciseToCamelCase(data): Exercise {
  const result: Exercise = {
    id: data.id,
    name: data.name,
    equipment: data.equipment,
    youtubeUrl: data.youtube_url,
    targetMuscle: data.target_muscle,
  };
  return result;
}

function mapWorkoutToCamelCase(data): Workout {
  const result: Workout = {
    id: data.id,
    type: data.type,
    workoutDate: data.workout_date,
    notes: data.notes,
  };
  return result;
}
