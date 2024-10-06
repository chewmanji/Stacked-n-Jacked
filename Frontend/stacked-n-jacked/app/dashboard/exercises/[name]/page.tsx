import { fetchExerciseDetails } from "@/app/lib/data";
import { Separator } from "@/components/ui/separator";
import {
  Table,
  TableHead,
  TableHeader,
  TableRow,
  TableCell,
  TableBody,
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
      <Table className="my-4">
        <TableHeader>
          <TableRow className="text-md">
            <TableHead>Target muscle</TableHead>
            <TableHead>Equipment</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow className="text-lg">
            <TableCell>{exercise.targetMuscle}</TableCell>
            <TableCell>{exercise.equipment ?? "---"}</TableCell>
          </TableRow>
        </TableBody>
      </Table>

      <Separator></Separator>
      <div className="text-center my-2 text-lg">Tutorial</div>
      <div className="relative w-full h-0 pb-[56.25%]">
        <iframe
          className="absolute top-0 left-0 w-full h-full"
          src={exercise.youtubeUrl?.replace("watch?v=", "embed/")}
          title={exercise.name}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>
      </div>
    </>
  );
}
