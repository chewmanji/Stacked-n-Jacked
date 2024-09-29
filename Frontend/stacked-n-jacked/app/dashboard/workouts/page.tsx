import { fetchWorkouts } from "@/app/lib/data";

export default async function Page() {
  const workouts = await fetchWorkouts();
  return (
    <div>
      {workouts.map((w) => {
        return <p key={w.id}>Workout at {w.workoutDate.toString()}</p>;
      })}
    </div>
  );
}
