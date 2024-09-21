import { Exercise } from "@/app/lib/definitions";

export async function fetchExercises(): Promise<Exercise[]> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises?limit=1000` //TODO consider pagination
  );

  const data: Exercise[] = await response.json();
  return convertKeysToCamelCase(data);
}

export async function fetchExerciseDetails(id: Number): Promise<Exercise> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/exercises/${id}`
  );

  const data: Exercise = await response.json();
  return convertKeysToCamelCase(data);
}

function snakeToCamel(str: string) {
  return str.replace(/(_\w)/g, (matches) => matches[1].toUpperCase());
}

function convertKeysToCamelCase(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map((item) => convertKeysToCamelCase(item));
  } else if (obj !== null && obj.constructor === Object) {
    return Object.keys(obj).reduce((acc, key) => {
      const camelKey = snakeToCamel(key);
      acc[camelKey] = convertKeysToCamelCase(obj[key]);
      return acc;
    }, {} as any);
  }
  return obj;
}
