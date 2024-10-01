import { z } from "zod";

export type Exercise = {
  id: number;
  name: string;
  targetMuscle: string;
  equipment: string | null;
  youtubeUrl: string | null;
};

export type ExerciseBackend = {
  id: number;
  name: string;
  target_muscle: string;
  equipment: string | null;
  youtube_url: string | null;
};

export type User = {
  id: number;
  email: string;
  birthDate: Date;
  gender: Gender;
};

export enum Gender {
  Male = 0,
  Female = 1,
  Unknown = 2,
}

export enum WorkoutType {
  FBW = "FBW",
  Push = "Push",
  Pull = "Pull",
  Upper = "Upper",
  Lower = "Lower",
  Custom = "Custom",
}

export type Workout = {
  id?: number;
  type: string;
  notes: string;
  workoutDate: Date;
};

export type WorkoutBackend = {
  id: number;
  type: string;
  notes: string;
  workout_date: Date;
};

export type WorkoutExercise = {
  id?: number;
  notes?: string;
  exercise: Exercise;
  workout: Workout;
  sets: ExerciseSet[];
};

export type WorkoutExerciseBackend = {
  id: number;
  notes?: string;
  exercise_id: number;
  workout_id: number;
};

export type ExerciseSet = {
  id?: number;
  repsCount: number;
  weight: number;
  setNumber: number;
  notes?: string;
  exercise: WorkoutExercise;
};

export type ExerciseSetBackend = {
  id: number;
  reps_count: number;
  weight: number | null;
  set_number: number;
  notes: string | null;
  workout_exercise_id: number;
};

export const SigninFormSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email." }).trim(),
  password: z.string().trim(),
});

export const SignupFormSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email." }).trim(),
  password: z
    .string()
    .min(8, { message: "Be at least 8 characters long" })
    .regex(/[a-zA-Z]/, { message: "Contain at least one letter." })
    .regex(/[0-9]/, { message: "Contain at least one number." })
    .regex(/[^a-zA-Z0-9]/, {
      message: "Contain at least one special character.",
    })
    .trim(),
  gender: z.number(),
  birthDate: z.string().date(),
});

export type FormState =
  | {
      errors?: {
        email?: string[];
        password?: string[];
      };
      message?: string;
    }
  | undefined;
