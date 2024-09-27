import { fetchWorkouts } from "@/app/lib/data";

export default async function Page() {
  const workouts = await fetchWorkouts();
  console.log(workouts);
  return (
    <div>
      {workouts.map((w) => {
        return <p>Workout at {w.workoutDate.toString()}</p>;
      })}
    </div>
  );
}
