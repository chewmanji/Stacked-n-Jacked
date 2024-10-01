"use client";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectItem,
  SelectContent,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Workout, WorkoutType } from "@/app/lib/definitions";
import { Dispatch, SetStateAction, useState } from "react";

export function EditWorkoutSheet({
  workout,
  setWorkout,
}: {
  workout: Workout;
  setWorkout: Dispatch<SetStateAction<Workout>>;
}) {
  const [type, setType] = useState<string>(workout.type);
  const [notes, setNotes] = useState<string>(workout.notes);
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline">Edit</Button>
      </SheetTrigger>
      <SheetContent side="bottom" className="h-[500px]">
        <SheetHeader>
          <SheetTitle>Edit workout </SheetTitle>
          <SheetDescription>
            Make changes to workout here. Click save when you&apos;re done.
          </SheetDescription>
        </SheetHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-5 items-center gap-4">
            <Label htmlFor="type" className="text-right">
              Type
            </Label>
            <Select
              defaultValue={workout.type}
              onValueChange={(v) => setType(v)}
            >
              <SelectTrigger className="col-span-4">
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                {Object.keys(WorkoutType).map((type) => {
                  return (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  );
                })}
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-5 items-center gap-4">
            <Label htmlFor="notes" className="text-right">
              Notes
            </Label>
            <Textarea
              defaultValue={workout.notes}
              placeholder="Type your notes here."
              className="col-span-4 w-full"
              onBlur={(e) => setNotes(e.target.value)}
            />
          </div>
        </div>
        <SheetClose asChild>
          <Button
            className="w-full"
            type="submit"
            onClick={() => {
              const workoutCopy = { ...workout };
              workoutCopy.notes = notes;
              workoutCopy.type = type;
              setWorkout(workoutCopy);
            }}
          >
            Save changes
          </Button>
        </SheetClose>
      </SheetContent>
    </Sheet>
  );
}
