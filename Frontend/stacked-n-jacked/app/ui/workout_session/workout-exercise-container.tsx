"use client";
import { Button } from "@/components/ui/button";
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
} from "@/components/ui/context-menu";
import { ExerciseSet, WorkoutExercise } from "@/app/lib/definitions";
import { SetsContainer } from "./set-container";

export function WorkoutExerciseContainer({
  workoutEx,
  handleAddSet,
  handleRemoveSet,
  handleEditSet,
  handleRemoveExercise,
}: {
  workoutEx: WorkoutExercise;
  handleAddSet: (workoutEx: WorkoutExercise) => void;
  handleRemoveSet: (workoutEx: WorkoutExercise) => void;
  handleEditSet: (set: ExerciseSet, workoutEx: WorkoutExercise) => void;
  handleRemoveExercise: (workoutEx: WorkoutExercise) => void;
}) {
  return (
    <AccordionItem value={workoutEx.exercise.name}>
      <ContextMenu>
        <ContextMenuTrigger>
          <AccordionTrigger>
            {workoutEx.id}. {workoutEx.exercise.name}
          </AccordionTrigger>
        </ContextMenuTrigger>

        <ContextMenuContent className="bg-destructive">
          <ContextMenuItem
            onClick={() => {
              handleRemoveExercise(workoutEx);
            }}
          >
            Delete
          </ContextMenuItem>
        </ContextMenuContent>
      </ContextMenu>
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
              size="default"
              variant="secondary"
              onClick={() => {
                handleRemoveSet(workoutEx);
              }}
            >
              Remove set
            </Button>
          </div>
        </div>
      </AccordionContent>
    </AccordionItem>
  );
}
