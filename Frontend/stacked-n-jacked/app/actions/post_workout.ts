"use server";

import { Workout, WorkoutExercise } from "../lib/definitions";
import { getToken } from "./auth";

export async function postWorkout(
  workout: Workout,
  workoutExercises: WorkoutExercise[]
): Promise<void | { message: string }> {
  const token = await getToken();
  const type = workout.type ? workout.type : null;
  console.log({
    type,
    notes: workout.notes,
    workoutExercises: workoutExercises.map((wEx) => ({
      exerciseId: wEx.exercise.id,
      ...wEx,
    })),
  });
  const body = JSON.stringify({
    type,
    notes: workout.notes,
    workoutExercises: workoutExercises.map((wEx) => ({
      exerciseId: wEx.exercise.id,
      ...wEx,
    })),
  });
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/workouts`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: body,
    }
  );
  if (!response.ok) {
    const error = await response.json();
    return {
      message: error.detail,
    };
  }
  const data: Workout = await response.json();
  //console.log(data);
  return;
}
// async function postWorkoutExercises(
//   workoutId: number,
//   workoutExercises: WorkoutExercise[],
//   token: string
// ) {
//   workoutExercises.forEach(async (workoutEx) => {
//     const response = await fetch(
//       `${process.env.NEXT_PUBLIC_API_BASE_URL}/workout_exercises`,
//       {
//         method: "POST",
//         headers: {
//           Authorization: `Bearer ${token}`,
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           workout_id: workoutId,
//           exercise_id: workoutEx.exercise.id,
//           notes: workoutEx.notes,
//         }),
//       }
//     );
//     if (!response.ok) {
//       console.log(response);
//       return;
//     }
//     const workoutExData: WorkoutExerciseBackend = await response.json();
//     const workoutExId: number = workoutExData.id;
//     await postSets(workoutExId, workoutEx.sets, token ?? "");
//   });
// }

// async function postSets(
//   workoutExId: number,
//   sets: ExerciseSet[],
//   token: string
// ) {
//   sets.forEach(async (s) => {
//     const response = await fetch(
//       `${process.env.NEXT_PUBLIC_API_BASE_URL}/sets`,
//       {
//         method: "POST",
//         headers: {
//           Authorization: `Bearer ${token}`,
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           workout_exercise_id: workoutExId,
//           set_number: s.setNumber,
//           notes: s.notes,
//           reps_count: s.repsCount,
//           weight: s.weight,
//         }),
//       }
//     );
//     if (!response.ok) {
//       console.log(response);
//       return;
//     }
//   });
// }
