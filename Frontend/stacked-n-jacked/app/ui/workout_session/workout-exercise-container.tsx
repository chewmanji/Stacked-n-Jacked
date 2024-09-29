"use client";
import { Button } from "@/components/ui/button";
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { ExerciseSet, WorkoutExercise } from "@/app/lib/definitions";
import { SetsContainer } from "./set-container";

export function WorkoutExerciseContainer({
  workoutEx,

  handleAddSet,
  handleRemoveSet,
}: {
  workoutEx: WorkoutExercise;
  workoutExercises: WorkoutExercise[];

  handleAddSet: any;
  handleRemoveSet: any;
}) {
  return (
    <AccordionItem value={workoutEx.exercise.name}>
      <AccordionTrigger>
        {workoutEx.id}. {workoutEx.exercise.name}
      </AccordionTrigger>
      <AccordionContent>
        <div className="flex flex-col items-center space-y-2">
          <SetsContainer workoutEx={workoutEx} />
          <div className="flex flex-col space-y-2 items-center ">
            <Button
              onClick={() => {
                handleAddSet(workoutEx);
              }}
            >
              Add set
            </Button>
            <Button
              size="sm"
              variant="destructive"
              onClick={() => {
                handleRemoveSet(workoutEx);
              }}
            >
              Remove
            </Button>
          </div>
        </div>
      </AccordionContent>
    </AccordionItem>
  );
}
