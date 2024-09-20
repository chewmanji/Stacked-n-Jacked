import { Exercise } from "@/app/lib/definitions";

export async function fetchExercises(): Promise<Exercise[]> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises?limit=1000` //TODO consider pagination
  );

  const data: Exercise[] = await response.json();
  return data;
}

export async function fetchExerciseDetails(id: Number): Promise<Exercise> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises/${id}` //TODO consider pagination
  );

  const data: Exercise = await response.json();
  return data;
}
