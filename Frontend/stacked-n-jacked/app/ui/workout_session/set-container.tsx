"use client";
import { WorkoutExerciseDetails, ExerciseSet } from "@/app/lib/definitions";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { PlusIcon, MinusIcon } from "lucide-react";
import { useState, Dispatch, SetStateAction, useEffect } from "react";

export function SetsContainer({
  workoutEx,
  handleEditSet,
}: {
  workoutEx: WorkoutExerciseDetails;
  handleEditSet: (set: ExerciseSet, workoutEx: WorkoutExerciseDetails) => void;
}) {
  return (
    <div>
      {workoutEx.sets.map((set, index) => {
        const previous = workoutEx.sets[index - 1]
          ? workoutEx.sets[index - 1]
          : set;
        return (
          <div key={set.setNumber} className="flex items-start space-x-4">
            <SetContainer
              set={set}
              previousSet={previous}
              workoutEx={workoutEx}
              handleEditSet={handleEditSet}
            />
          </div>
        );
      })}
    </div>
  );
}

export function SetContainer({
  set,
  previousSet,
  workoutEx,
  handleEditSet,
}: {
  set: ExerciseSet;
  previousSet: ExerciseSet;
  workoutEx: WorkoutExerciseDetails;
  handleEditSet: (set: ExerciseSet, workoutEx: WorkoutExerciseDetails) => void;
}) {
  const [reps, setReps] = useState(set.repsCount || previousSet.repsCount);
  const [weight, setWeight] = useState(set.weight || previousSet.weight);
  useEffect(() => {
    set.repsCount = reps;
    set.weight = weight;
    handleEditSet(set, workoutEx);
  }, [reps, weight]);
  return (
    <div>
      <div className="flex flex-col items-center">
        <p className="text-lg mt-2 mb-2">Set {set.setNumber}</p>
        <Label className="my-2 font-bold">Reps</Label>
        <div className="flex items-center space-x-2">
          <AddButton setState={setReps} value={1} />
          <Input
            value={reps !== 0 ? reps : ""}
            onChange={(e) => setReps(Math.floor(Number(e.target.value)))}
            type="number"
            placeholder="Reps count"
            className="w-24"
          />
          <MinusButton setState={setReps} value={1} />
        </div>
        <Label className="my-2 font-bold">Weight</Label>
        <div className="flex items-center space-x-2">
          <AddButton setState={setWeight} value={1.25} />

          <Input
            value={weight > 0 ? weight : ""}
            onChange={(e) => setWeight(Number(e.target.value))}
            type="number"
            placeholder="Weight"
            className="w-24"
          />

          <MinusButton setState={setWeight} value={1.25} />
        </div>
      </div>
    </div>
  );
}

function AddButton({
  setState,
  value,
}: {
  setState: Dispatch<SetStateAction<number>>;
  value: number;
}) {
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() =>
        setState((prevState) => {
          return prevState + value;
        })
      }
    >
      <PlusIcon />
    </Button>
  );
}

function MinusButton({
  setState,
  value,
}: {
  setState: Dispatch<SetStateAction<number>>;
  value: number;
}) {
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() =>
        setState((prevState) => {
          if (prevState <= 0) return 0;
          return prevState - value;
        })
      }
    >
      <MinusIcon />
    </Button>
  );
}
