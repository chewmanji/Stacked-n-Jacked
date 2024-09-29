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
  WorkoutExercise,
  ExerciseSet,
  Exercise,
} from "@/app/lib/definitions";
import { useTableConfig } from "@/app/hooks/useTableConfig";
import { WorkoutExerciseContainer } from "@/app/ui/workout_session/workout-exercise-container";
import { Accordion } from "@/components/ui/accordion";

export function SearchTable({
  columns,
  data,
  targetMuscles,
}: {
  columns: ColumnDef<Exercise, any>[];
  data: Exercise[];
  targetMuscles: string[];
}) {
  const [selectedMuscle, setSelectedMuscle] = useState<string>();
  const { table } = useTableConfig(data, columns);

  const [workout, setWorkout] = useState<Workout>(() => {
    return { workoutDate: new Date() };
  });

  const [workoutExercises, setWorkoutExercises] = useState<WorkoutExercise[]>(
    []
  );

  function handleAddExercise(ex: Exercise) {
    const exs = [...workoutExercises];
    const workoutEx: WorkoutExercise = {
      id: exs.length + 1,
      exercise: ex,
      workout: workout,
      sets: [],
    };
    exs.push(workoutEx);
    setWorkoutExercises(exs);
  }

  function handleAddSet(workoutEx: WorkoutExercise) {
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

  function handleRemoveSet(workoutEx: WorkoutExercise) {
    const updatedExercises = workoutExercises.map((ex) =>
      ex.exercise.id === workoutEx.exercise.id
        ? { ...ex, sets: [...ex.sets.slice(0, -1)] }
        : ex
    );
    setWorkoutExercises(updatedExercises);
  }

  function handleEditSet(set: ExerciseSet, workoutEx: WorkoutExercise) {}
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

  useEffect(() => {
    table.getColumn("targetMuscle")?.setFilterValue(selectedMuscle);
  }, [selectedMuscle, table]);

  return (
    <div>
      <div>
        <p>Workout</p>
        <Accordion type="single" collapsible>
          {workoutExercises.map((workoutEx) => {
            return (
              <div key={workoutEx.exercise.id}>
                <WorkoutExerciseContainer
                  workoutEx={workoutEx}
                  workoutExercises={workoutExercises}
                  handleAddSet={handleAddSet}
                  handleRemoveSet={handleRemoveSet}
                />
              </div>
            );
          })}
        </Accordion>
      </div>
      <div className="flex items-center py-4">
        <Input
          placeholder="Search exercise..."
          value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("name")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
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
              table.getRowModel().rows.map((row) => (
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
                  <TableCell key={row.original.id}>
                    <div>
                      <Button
                        disabled={workoutExercises
                          .map((e) => e.exercise.id)
                          .includes(row.original.id)}
                        onClick={() => handleAddExercise(row.original)} //probably to refactor -> remove row if included in exs
                      >
                        Add
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
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
