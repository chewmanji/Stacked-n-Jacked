import { z } from "zod";

export type Exercise = {
  id: number;
  name: string;
  targetMuscle: string;
  equipment: string | null;
  youtubeUrl: string | null;
};

export type ExerciseChartData = {
  id: number;
  name: string;
  workoutExercisesDetails: WorkoutExerciseDetails[];
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
  Other = 2,
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

export type WorkoutDetails = {
  id: number;
  type: string;
  notes: string;
  workoutDate: Date;
  workoutExercises: WorkoutExerciseDetails[];
};

export type WorkoutExercise = {
  id: number;
  workoutId: number;
  exerciseId: number;
  notes: string | null;
};

export type WorkoutExerciseDetails = {
  id?: number;
  notes?: string;
  exercise: Exercise;
  sets: ExerciseSet[];
  workout?: Workout;
  workoutDate?: Date;
};

export type ExerciseSet = {
  id?: number;
  repsCount: number;
  weight: number;
  setNumber: number;
  notes?: string;
  exercise?: WorkoutExerciseDetails;
};

export const SignInFormSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email." }).trim(),
  password: z.string().trim(),
});

export const SignUpFormSchema = z
  .object({
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
    confirmPassword: z.string(),
    gender: z.string(),
    birthDate: z.date(),
    isVerified: z.boolean().optional(),
  })
  .superRefine(({ confirmPassword, password }, ctx) => {
    if (confirmPassword !== password) {
      ctx.addIssue({
        code: "custom",
        message: "The passwords did not match",
        path: ["confirmPassword"],
      });
    }
  });

export const ChangeEmailFormSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email." }).trim(),
});

export const ChangePasswordFormSchema = z
  .object({
    newPassword: z
      .string()
      .min(8, { message: "Be at least 8 characters long" })
      .regex(/[a-zA-Z]/, { message: "Contain at least one letter." })
      .regex(/[0-9]/, { message: "Contain at least one number." })
      .regex(/[^a-zA-Z0-9]/, {
        message: "Contain at least one special character.",
      })
      .trim(),

    confirmPassword: z.string(),
  })
  .superRefine(({ confirmPassword, newPassword }, ctx) => {
    if (confirmPassword !== newPassword) {
      ctx.addIssue({
        code: "custom",
        message: "The passwords did not match",
        path: ["confirmPassword"],
      });
    }
  });

export const EditProfileFormSchema = z.object({
  gender: z.string().optional(),
  birthDate: z.date().optional(),
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
