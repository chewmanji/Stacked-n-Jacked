import {
  Exercise,
  Workout,
  User,
  WorkoutDetails,
  WorkoutExerciseDetails,
} from "@/app/lib/definitions";
import { getToken } from "../actions/auth";

export async function fetchExercises(): Promise<Exercise[]> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises?limit=1000`
  );

  const data: Exercise[] = await response.json();
  return data;
}

export async function fetchExerciseDetails(id: number): Promise<Exercise> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises/${id}`
  );

  const data: Exercise = await response.json();
  return data;
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

  const data: Workout[] = await response.json();
  return data;
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
  const data: WorkoutDetails = await response.json();
  return data;
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

  const data: User = await response.json();

  return { ...data, birthDate: new Date(data.birthDate) };
}

export async function fetchDataForChart(
  id: number
): Promise<WorkoutExerciseDetails[]> {
  const token = await getToken();
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/workout_exercises/exercises/${id}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data: WorkoutExerciseDetails[] = await response.json();
  console.log(data);
  return data;
}

export async function fetchExercisesFromWorkoutExercises(): Promise<
  Exercise[]
> {
  const token = await getToken();
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/workout_exercises/exercises`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data: Exercise[] = await response.json();
  return data;
}

export async function fetchLatestExercises(): Promise<Exercise[]> {
  const token = await getToken();
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/workout_exercises/exercises/latest`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data: Exercise[] = await response.json();
  return data;
}
