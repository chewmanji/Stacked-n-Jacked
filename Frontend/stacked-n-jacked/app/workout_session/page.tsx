import { SearchTable } from "@/app/ui/workout_session/search-table";
import { columns } from "@/app/ui/workout_session/columns";
import { fetchLatestExercises } from "../lib/data";

export default async function Page() {
  const latestExercises = await fetchLatestExercises();

  const targetMuscles = latestExercises.map((ex) => ex.targetMuscle);
  const muscles = Array.from(new Set(targetMuscles));

  return (
    <div className="container mx-auto py-5 ">
      <SearchTable
        data={latestExercises ?? []}
        columns={columns}
        targetMuscles={muscles}
      ></SearchTable>
    </div>
  );
}
