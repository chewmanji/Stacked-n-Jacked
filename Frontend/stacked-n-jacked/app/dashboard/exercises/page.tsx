import { fetchExercises } from "@/app/lib/data";
import { ExerciseTable } from "@/app/ui/dashboard/exercises/table";
import { columns } from "@/app/ui/dashboard/exercises/columns";

export default async function Page() {
  const exercises = await fetchExercises();
  const targetMuscles = exercises.map((ex) => ex.targetMuscle);
  const uniqueTargetMuscles = Array.from(new Set(targetMuscles));
  return (
    <>
      <p className="text-3xl">Exercises</p>
      <div>
        <ExerciseTable
          columns={columns}
          data={exercises}
          targetMuscles={uniqueTargetMuscles}
        ></ExerciseTable>
      </div>
    </>
  );
}
