import { SearchTable } from "@/app/ui/workout_session/search-table";
import { columns } from "@/app/ui/workout_session/columns";
import { fetchExercises } from "../lib/data";

export default async function Page() {
  const exercises = await fetchExercises();

  const targetMuscles = exercises.map((ex) => ex.targetMuscle);
  const muscles = Array.from(new Set(targetMuscles));

  return (
    <div className="container mx-auto py-10">
      <SearchTable
        data={exercises ?? []}
        columns={columns}
        targetMuscles={muscles}
      ></SearchTable>
    </div>
  );
}
