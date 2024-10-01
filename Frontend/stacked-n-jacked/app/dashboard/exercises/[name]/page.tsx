import { fetchExerciseDetails } from "@/app/lib/data";
import {
  Table,
  TableBody,
  TableHead,
  TableCell,
  TableRow,
} from "@/components/ui/table";

export default async function Page({
  searchParams,
}: {
  searchParams?: { [key: string]: string | string[] };
}) {
  const exercise = await fetchExerciseDetails(Number(searchParams?.id));
  return (
    <>
      <p className="text-3xl">{exercise.name}</p>
      <div className="container mx-auto py-10">
        <Table>
          <TableBody>
            <TableRow>
              <TableHead>Target Muscle</TableHead>
              <TableCell>{exercise.targetMuscle}</TableCell>
            </TableRow>
            <TableRow>
              <TableHead>Equipment</TableHead>
              <TableCell>{exercise.equipment ?? "---"}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="text-center">Tutorial</TableCell>
              <TableCell>
                <div className="relative w-full h-0 pb-[56.25%]">
                  {/* 16:9 aspect ratio */}
                  <iframe
                    className="absolute top-0 left-0 w-full h-full"
                    src={exercise.youtubeUrl?.replace("watch?v=", "embed/")}
                    title={exercise.name}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  ></iframe>
                </div>
                {/* AI GENERATED - to fix */}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </>
  );
}
