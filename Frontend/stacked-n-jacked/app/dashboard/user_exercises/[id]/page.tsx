import { fetchDataForChart } from "@/app/lib/data";
import { ExerciseChart } from "@/app/ui/user_exercises/exercise_chart";
import moment from "moment";

export default async function Page({
  params,
  searchParams,
}: {
  params: { id: number; name: string };
  searchParams: { name: string };
}) {
  const data = await fetchDataForChart(params.id);
  data.sort(
    (a, b) =>
      moment(a.workoutDate).toDate().getTime() -
      moment(b.workoutDate).toDate().getTime()
  );

  return (
    <div>
      <ExerciseChart data={data} chartTitle={searchParams.name} />
    </div>
  );
}
