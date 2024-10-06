"use client";

import { Exercise } from "@/app/lib/definitions";
import { ColumnDef } from "@tanstack/react-table";
import Link from "next/link";
import slugify from "slugify";
import { ArrowUpDown } from "lucide-react";
import { Button } from "@/components/ui/button";

export const columns: ColumnDef<Exercise>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Exercise
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
  },
  {
    accessorKey: "targetMuscle",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Target muscle
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
    filterFn: "arrIncludesSome",
  },

  {
    accessorKey: "details",
    header: "Details",
    cell: ({ row }) => {
      return (
        <div className="text-primary">
          <Link
            href={{
              pathname: `/dashboard/exercises/${slugify(row.original.name, {
                lower: true,
              })}`,
              query: { id: row.original.id },
            }}
          >
            Details
          </Link>
        </div>
      );
    },
  },
];
