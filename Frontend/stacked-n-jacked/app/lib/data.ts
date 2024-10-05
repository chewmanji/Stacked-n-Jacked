import { Exercise, Workout, User, WorkoutDetails } from "@/app/lib/definitions";
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
  // const workoutExs: WorkoutExercise[] = data.workout_exercises.map((wEx) => ({
  //   id: wEx.id,
  //   exercise: mapExerciseToCamelCase(wEx.exercise),
  //   sets: wEx.sets.map((s) => ({
  //     id: s.id,
  //     repsCount: s.reps_count,
  //     weight: s.weight ?? 0,
  //     setNumber: s.set_number,
  //   })),
  // }));
  // const workout: WorkoutDetails = {
  //   id: data.id,
  //   type: data.type,
  //   notes: data.notes,
  //   workoutDate: data.workout_date,
  //   workoutExercises: workoutExs,
  // };
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

  return data;
}

// function mapExerciseToCamelCase(data: Exercise): Exercise {
//   const result: Exercise = {
//     id: data.id,
//     name: data.name,
//     equipment: data.equipment,
//     youtubeUrl: data.youtube_url,
//     targetMuscle: data.target_muscle,
//   };
//   return result;
// }

// function mapWorkoutToCamelCase(data: Workout): Workout {
//   const result: Workout = {
//     id: data.id,
//     type: data.type,
//     workoutDate: new Date(data.workout_date),
//     notes: data.notes,
//   };
//   return result;
// }
