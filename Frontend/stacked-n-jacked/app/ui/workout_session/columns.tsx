"use client";

import { Exercise } from "@/app/lib/definitions";
import { ColumnDef } from "@tanstack/react-table";

export const columns: ColumnDef<Exercise>[] = [
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "targetMuscle",
    header: "Target muscle",
    filterFn: "includesString",
  },
];
