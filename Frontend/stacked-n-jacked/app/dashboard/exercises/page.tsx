import { fetchExercises } from "@/app/lib/data";
import { DataTable } from "@/app/ui/dashboard/exercises/data-table";
import { columns } from "@/app/ui/dashboard/exercises/columns";

export default async function Page() {
  const exercises = await fetchExercises();
  const targetMuscles = exercises.map((ex) => ex.targetMuscle); //move it to server side???
  const uniqueTargetMuscles = Array.from(new Set(targetMuscles));
  return (
    <>
      <p className="text-3xl">Exercises</p>
      <div className="container mx-auto py-10">
        <DataTable
          columns={columns}
          data={exercises}
          targetMuscles={uniqueTargetMuscles}
        ></DataTable>
      </div>
    </>
  );
}
