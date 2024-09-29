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
  handleEditSet,
}: {
  workoutEx: WorkoutExercise;
  handleAddSet: (workoutEx: WorkoutExercise) => void;
  handleRemoveSet: (workoutEx: WorkoutExercise) => void;
  handleEditSet: (set: ExerciseSet, workoutEx: WorkoutExercise) => void;
}) {
  return (
    <AccordionItem value={workoutEx.exercise.name}>
      <AccordionTrigger>
        {workoutEx.id}. {workoutEx.exercise.name}
      </AccordionTrigger>
      <AccordionContent>
        <div className="flex flex-col items-center space-y-2">
          <SetsContainer workoutEx={workoutEx} handleEditSet={handleEditSet} />
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
              variant="secondary"
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
