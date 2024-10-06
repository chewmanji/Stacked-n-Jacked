import { fetchWorkouts } from "@/app/lib/data";
import Link from "next/link";
import moment from "moment";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

export default async function Page() {
  const workouts = await fetchWorkouts();
  workouts.sort(
    (a, b) =>
      moment(a.workoutDate).toDate().getTime() -
      moment(b.workoutDate).toDate().getTime()
  );
  return (
    <div>
      {workouts.map((w) => {
        return (
          <div
            className="my-4 grid grid-cols-4 items-center text-center"
            key={w.id}
          >
            <div className="col-span-2">
              Workout at {moment(w.workoutDate).format("YYYY MMM DD")}{" "}
            </div>
            <span>{w.type ? `(${w.type})` : ""}</span>

            <Link className="text-primary" href={`/dashboard/workouts/${w.id}`}>
              <Button variant="outline">Details</Button>
            </Link>
            <Separator className="mt-4 col-span-4" />
          </div>
        );
      })}
    </div>
  );
}
