import { fetchWorkoutDetails } from "@/app/lib/data";
import { WorkoutDetailsComponent } from "@/app/ui/dashboard/workouts/[id]/workout-details-components";
import { Label } from "@/components/ui/label";
import moment from "moment";

export default async function Page({ params }: { params: { id: number } }) {
  const workoutDetails = await fetchWorkoutDetails(params.id);
  return (
    <div>
      <div className="mb-4 text-xl font-medium text-center">
        {moment(workoutDetails.workoutDate).format("YYYY MMMM DD")}
      </div>
      <Label htmlFor="notes">Notes</Label>
      <p className="italic mb-4">{workoutDetails.notes}</p>
      <WorkoutDetailsComponent
        workoutDetails={workoutDetails}
      ></WorkoutDetailsComponent>
    </div>
  );
}
