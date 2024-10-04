import {
  Exercise,
  Workout,
  WorkoutBackend,
  ExerciseBackend,
  User,
  WorkoutDetailsBackend,
  WorkoutDetails,
  WorkoutExercise,
} from "@/app/lib/definitions";
import { getToken } from "../actions/auth";

export async function fetchExercises(): Promise<Exercise[]> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises?limit=1000`
  );

  const data: ExerciseBackend[] = await response.json();
  return data.map((ex) => mapExerciseToCamelCase(ex));
}

export async function fetchExerciseDetails(id: number): Promise<Exercise> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises/${id}`
  );

  const data: ExerciseBackend = await response.json();
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

  const data: WorkoutBackend[] = await response.json();
  return data.map((w) => mapWorkoutToCamelCase(w));
}

export async function fetchWorkoutDetails(id: number): Promise<WorkoutDetails> {
  const token = await getToken();
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/workouts/${id}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  const data: WorkoutDetailsBackend = await response.json();
  const workoutExs: WorkoutExercise[] = data.workout_exercises.map((wEx) => ({
    id: wEx.id,
    exercise: mapExerciseToCamelCase(wEx.exercise),
    sets: wEx.sets.map((s) => ({
      id: s.id,
      repsCount: s.reps_count,
      weight: s.weight ?? 0,
      setNumber: s.set_number,
    })),
  }));
  const workout: WorkoutDetails = {
    id: data.id,
    type: data.type,
    notes: data.notes,
    workoutDate: data.workout_date,
    workoutExercises: workoutExs,
  };
  return workout;
}

export async function fetchCurrentUser(): Promise<User> {
  const token = await getToken();
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/users/me`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data: {
    email: string;
    birth_date: string;
    gender: number;
    id: number;
  } = await response.json();

  return {
    email: data.email,
    birthDate: new Date(data.birth_date),
    gender: data.gender,
    id: data.id,
  };
}

function mapExerciseToCamelCase(data: ExerciseBackend): Exercise {
  const result: Exercise = {
    id: data.id,
    name: data.name,
    equipment: data.equipment,
    youtubeUrl: data.youtube_url,
    targetMuscle: data.target_muscle,
  };
  return result;
}

function mapWorkoutToCamelCase(data: WorkoutBackend): Workout {
  const result: Workout = {
    id: data.id,
    type: data.type,
    workoutDate: new Date(data.workout_date),
    notes: data.notes,
  };
  return result;
}
