"use server";

import { Workout, WorkoutExerciseDetails } from "../lib/definitions";
import { getToken } from "./auth";

export async function postWorkout(
  workout: Workout,
  workoutExercises: WorkoutExerciseDetails[]
): Promise<void | { message: string }> {
  const token = await getToken();
  const type = workout.type ? workout.type : null;
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
  console.log(data);
  return;
}
