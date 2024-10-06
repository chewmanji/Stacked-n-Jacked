import { fetchExercisesFromWorkoutExercises } from "@/app/lib/data";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Separator } from "@/components/ui/separator";

export default async function Page() {
  const exercises = await fetchExercisesFromWorkoutExercises();
  return (
    <div>
      {exercises.map((ex) => (
        <>
          <div
            key={ex.id}
            className="flex justify-between mx-2 my-4 items-center"
          >
            <span>{ex.name}</span>
            <Link
              href={{
                pathname: `/dashboard/user_exercises/${ex.id}`,
                query: { name: ex.name },
              }}
            >
              <Button>Details</Button>
            </Link>
          </div>
          <Separator></Separator>
        </>
      ))}
    </div>
  );
}
