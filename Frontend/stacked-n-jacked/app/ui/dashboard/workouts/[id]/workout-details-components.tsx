"use client";
import { WorkoutDetails, WorkoutExerciseDetails } from "@/app/lib/definitions";
import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export function WorkoutDetailsComponent({
  workoutDetails,
}: {
  workoutDetails: WorkoutDetails;
}) {
  return (
    <div>
      {workoutDetails.workoutExercises.map((ex, i) => (
        <div className="py-4" key={ex.id}>
          <span className="font-semibold">
            {i + 1}. {ex.exercise.name}
          </span>
          <WorkoutExerciseTable
            workoutExercise={ex}
            key={ex.id}
          ></WorkoutExerciseTable>
        </div>
      ))}
    </div>
  );
}

function WorkoutExerciseTable({
  workoutExercise,
}: {
  workoutExercise: WorkoutExerciseDetails;
}) {
  const totalVolume: number = workoutExercise.sets.reduce(
    (total, currentSet) => total + currentSet.weight * currentSet.repsCount,
    0
  );
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Set No.</TableHead>
          <TableHead>Reps</TableHead>
          <TableHead className="text-right">Weight</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {workoutExercise.sets
          .sort((a, b) => a.setNumber - b.setNumber)
          .map((set) => (
            <TableRow key={set.id}>
              <TableCell>{set.setNumber}.</TableCell>
              <TableCell>{set.repsCount}</TableCell>
              <TableCell className="text-right">{set.weight} kg</TableCell>
            </TableRow>
          ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={2}>Total</TableCell>
          <TableCell className="text-right">{totalVolume} KG</TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  );
}
