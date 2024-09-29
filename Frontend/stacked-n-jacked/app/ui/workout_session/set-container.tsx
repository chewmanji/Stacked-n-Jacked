"use client";
import { WorkoutExercise, ExerciseSet } from "@/app/lib/definitions";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { PlusIcon, MinusIcon } from "lucide-react";
import { useState, Dispatch, SetStateAction } from "react";

export function SetsContainer({ workoutEx }: { workoutEx: WorkoutExercise }) {
  return (
    <div>
      {workoutEx.sets.map((set, index) => {
        let previous;
        if (index !== 0) {
          previous = workoutEx.sets[index];
        }
        return (
          <div key={set.setNumber} className="flex items-start space-x-4">
            <SetContainer set={set} previousSet={previous} />
          </div>
        );
      })}
    </div>
  );
}

export function SetContainer({
  set,
  previousSet,
}: {
  set: ExerciseSet;
  previousSet?: ExerciseSet;
}) {
  console.log(previousSet);
  const [reps, setReps] = useState(previousSet?.repsCount ?? 0);
  const [weight, setWeight] = useState(previousSet?.weight ?? 0);
  return (
    <div>
      <p className="mt-2 mb-2">Set {set.setNumber}</p>
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
