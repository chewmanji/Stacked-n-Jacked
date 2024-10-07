"use client";

import { ColumnDef, flexRender } from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import {
  DoubleArrowLeftIcon,
  DoubleArrowRightIcon,
  ChevronRightIcon,
  ChevronLeftIcon,
} from "@radix-ui/react-icons";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";

import {
  Workout,
  WorkoutExerciseDetails,
  ExerciseSet,
  Exercise,
} from "@/app/lib/definitions";
import { useTableConfig } from "@/app/hooks/useTableConfig";
import { WorkoutExerciseContainer } from "@/app/ui/workout_session/workout-exercise-container";
import { Accordion } from "@/components/ui/accordion";
import { EditWorkoutSheet } from "./edit-workout-sheet";
import { CancelWorkoutDialog } from "./cancel-workout-dialog";
import { postWorkout } from "@/app/actions/post_workout";
import { useRouter } from "next/navigation";
import { ButtonLoading } from "../button-loading";
import { useToast } from "@/hooks/use-toast";

export function SearchTable({
  columns,
  data,
  targetMuscles,
}: {
  columns: ColumnDef<Exercise | unknown>[];
  data: Exercise[];
  targetMuscles: string[];
}) {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedMuscle, setSelectedMuscle] = useState<string>();
  const { table } = useTableConfig(data, columns);
  const { toast } = useToast();

  const [workout, setWorkout] = useState<Workout>({
    workoutDate: new Date(),
    notes: "",
    type: "",
  });
  const [workoutExercises, setWorkoutExercises] = useState<
    WorkoutExerciseDetails[]
  >([]);

  function handleAddExercise(ex: Exercise) {
    const exs = [...workoutExercises];
    const workoutEx: WorkoutExerciseDetails = {
      id: exs.length + 1,
      exercise: ex,
      workout: workout,
      sets: [],
    };
    exs.push(workoutEx);
    setWorkoutExercises(exs);
  }

  function handleRemoveExercise(workoutEx: WorkoutExerciseDetails) {
    const exs = workoutExercises.filter((ex) => ex.id !== workoutEx.id);
    exs.forEach((ex, index) => (ex.id = index + 1));
    setWorkoutExercises(exs);
  }

  function handleAddSet(workoutEx: WorkoutExerciseDetails) {
    const set: ExerciseSet = {
      exercise: workoutEx,
      repsCount: 0,
      weight: 0,
      setNumber: workoutEx.sets.length + 1,
    };
    const updatedExercises = workoutExercises.map((ex) =>
      ex.exercise.id === workoutEx.exercise.id
        ? { ...ex, sets: [...ex.sets, set] }
        : ex
    );

    setWorkoutExercises(updatedExercises);
  }

  function handleRemoveSet(workoutEx: WorkoutExerciseDetails) {
    const updatedExercises = workoutExercises.map((ex) =>
      ex.exercise.id === workoutEx.exercise.id
        ? { ...ex, sets: [...ex.sets.slice(0, -1)] }
        : ex
    );
    setWorkoutExercises(updatedExercises);
  }

  function handleEditSet(set: ExerciseSet, workoutEx: WorkoutExerciseDetails) {
    const setsCopy = [...workoutEx.sets];
    const index = setsCopy.findIndex((s) => s.setNumber === set.setNumber);
    setsCopy[index] = set;

    const updatedExercises = workoutExercises.map((ex) =>
      ex.exercise.id === workoutEx.exercise.id
        ? { ...ex, sets: [...setsCopy] }
        : ex
    );
    setWorkoutExercises(updatedExercises);
  }

  const handleMuscleClick = (muscle: string) => {
    switch (muscle) {
      case "reset":
        setSelectedMuscle("");
        break;
      default:
        setSelectedMuscle(muscle);
        break;
    }
  };

  async function handleSaveWorkout() {
    if (!isSubmitting) {
      setIsSubmitting(true);
      const message = await postWorkout(workout, workoutExercises);
      if (message) {
        toast({
          title: "Error",
          variant: "destructive",
          description: message.message,
        });
      } else {
        toast({
          title: "Success",
          description: "Workout saved!",
          duration: 2000,
        });
        router.replace("/dashboard");
      }
    }

    setIsSubmitting(false);
  }

  useEffect(() => {
    table.getColumn("targetMuscle")?.setFilterValue(selectedMuscle);
  }, [selectedMuscle, table]);

  return (
    <div className="mx-2">
      <div className="flex flex-col items-center  mb-6">
        <h2 className="text-center text-lg">Workout</h2>
        <EditWorkoutSheet workout={workout} setWorkout={setWorkout} />
      </div>

      <div>
        <Accordion type="single" collapsible>
          {workoutExercises.map((workoutEx) => {
            return (
              <div key={workoutEx.exercise.id}>
                <WorkoutExerciseContainer
                  workoutEx={workoutEx}
                  handleAddSet={handleAddSet}
                  handleRemoveSet={handleRemoveSet}
                  handleEditSet={handleEditSet}
                  handleRemoveExercise={handleRemoveExercise}
                />
              </div>
            );
          })}
        </Accordion>
      </div>
      <div className="flex justify-between w-full px-4 mt-4">
        <CancelWorkoutDialog />
        {isSubmitting ? (
          <ButtonLoading />
        ) : (
          <Button
            onClick={async () => await handleSaveWorkout()}
            disabled={workoutExercises.length === 0}
          >
            Save
          </Button>
        )}
      </div>
      <div className="flex flex-col items-center  mt-3">
        <h2 className="text-center text-lg">Choose exercises</h2>
      </div>
      <div className="flex items-center py-4">
        <Input
          placeholder="Search exercise..."
          value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("name")?.setFilterValue(event.target.value)
          }
          className="max-w"
        />
      </div>
      <div className="flex-wrap items-center pb-4">
        <Select onValueChange={handleMuscleClick} defaultValue="">
          <SelectTrigger>
            <SelectValue placeholder="Filter by target muscle" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="reset">---</SelectItem>
            {targetMuscles.map((targetMuscle) => {
              return (
                <SelectItem key={targetMuscle} value={targetMuscle}>
                  {targetMuscle}
                </SelectItem>
              );
            })}
          </SelectContent>
        </Select>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => {
                const rowData = row.original as Exercise;
                return (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && "selected"}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </TableCell>
                    ))}
                    <TableCell key={rowData.id}>
                      <div>
                        <Button
                          disabled={workoutExercises
                            .map((e) => e.exercise.id)
                            .includes(rowData.id)}
                          onClick={() => handleAddExercise(rowData)}
                        >
                          Add
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex mt-2 mb-2 w-[100px] items-center justify-center text-sm font-medium">
        Page {table.getState().pagination.pageIndex + 1} of{" "}
        {table.getPageCount()}
      </div>
      <div className="flex items-center space-x-2">
        <Button
          variant="outline"
          className="hidden h-8 w-8 p-0 lg:flex"
          onClick={() => table.setPageIndex(0)}
          disabled={!table.getCanPreviousPage()}
        >
          <span className="sr-only">Go to first page</span>
          <DoubleArrowLeftIcon className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          className="h-8 w-8 p-0"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          <span className="sr-only">Go to previous page</span>
          <ChevronLeftIcon className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          className="h-8 w-8 p-0"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          <span className="sr-only">Go to next page</span>
          <ChevronRightIcon className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          className="hidden h-8 w-8 p-0 lg:flex"
          onClick={() => table.setPageIndex(table.getPageCount() - 1)}
          disabled={!table.getCanNextPage()}
        >
          <span className="sr-only">Go to last page</span>
          <DoubleArrowRightIcon className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
