import { fetchExercises } from "@/app/lib/data";
import { DataTable } from "@/app/ui/dashboard/exercises/data-table";
import { columns } from "@/app/ui/dashboard/exercises/columns";

export default async function Page() {
  const exercises = await fetchExercises();
  return (
    <div className="container mx-auto py-10">
      <DataTable columns={columns} data={exercises}></DataTable>
    </div>
  );
}
