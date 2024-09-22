import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Table } from "@tanstack/react-table";

export default function MuscleButton<TData>({
  muscle,
  table,
}: {
  muscle: string;
  table: Table<TData>;
}) {
  const [isChosen, setChosen] = useState(false);

  return (
    <Button
      onClick={() => {
        setChosen(!isChosen);
        table.getColumn("targetMuscle")?.setFilterValue(muscle);
      }}
      className={`${
        isChosen ? "bg-white text-black" : ""
      } hover:bg-white hover:text-black`}
    >
      {muscle}
    </Button>
  );
}
