import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import Link from "next/link";
export default function Page() {
  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <Link href="/workout_session">
        <Button variant="default" className="h-20 rounded-md px-8">
          <Plus className="h-24 w-24 text-foreground-primary"></Plus>
        </Button>
      </Link>

      <p className="my-4">Time to crush it!</p>
    </div>
  );
}
