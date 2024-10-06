"use client";

import { WorkoutExerciseDetails } from "@/app/lib/definitions";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts";
import moment from "moment";
import { useState } from "react";

const chartConfig = {
  total: {
    label: "Total",
    color: "hsl(var(--chart-2))",
  },
  avgPerRep: {
    label: "AVG KGs/rep",
    color: "hsl(var(--chart-5))",
  },
} satisfies ChartConfig;

export function ExerciseChart({
  data,
  chartTitle,
}: {
  data: WorkoutExerciseDetails[];
  chartTitle: string;
}) {
  const [activeChart, setActiveChart] =
    useState<keyof typeof chartConfig>("total");

  function avgFunc(wEx: WorkoutExerciseDetails) {
    const res = wEx.sets.reduce(
      (acc: { sum: number; n: number }, currentSet) => {
        return {
          sum: acc.sum + currentSet.weight * currentSet.repsCount,
          n: acc.n + currentSet.repsCount,
        };
      },
      { sum: 0, n: 0 }
    );
    return (res.sum / res.n).toFixed(2);
  }

  const chartData = Array.from(data, (e) => ({
    date: e.workoutDate,
    total: e.sets
      .reduce(
        (total, currentSet) => total + currentSet.weight * currentSet.repsCount,
        0
      )
      .toFixed(2),
    avgPerRep: avgFunc(e),
  }));
  return (
    <Card>
      <CardHeader className="flex flex-col items-stretch space-y-0 border-b p-0 sm:flex-row">
        <div className="flex flex-1 flex-col gap-1 px-6 py-5 sm:py-6">
          <CardTitle>{chartTitle}</CardTitle>
          <CardDescription>
            {moment(data[0].workoutDate).format("MMM YYYY")} -{" "}
            {moment(data[data.length - 1].workoutDate).format("MMM YYYY")}
          </CardDescription>
        </div>
        <div className="flex">
          {["total", "avgPerRep"].map((key) => {
            const chart = key as keyof typeof chartConfig;
            return (
              <button
                key={chart}
                data-active={activeChart === chart}
                className="flex flex-1 flex-col justify-center gap-1 border-t px-6 py-4 items-center even:border-l data-[active=true]:bg-muted/50 sm:border-l sm:border-t-0 sm:px-8 sm:py-6"
                onClick={() => setActiveChart(chart)}
              >
                <span className="text-xs">{chartConfig[chart].label}</span>
              </button>
            );
          })}
        </div>
      </CardHeader>
      <CardContent className="p-2">
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <LineChart
            accessibilityLayer
            data={chartData}
            margin={{
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              padding={{ left: 4 }}
              minTickGap={16}
              tickFormatter={(v) => moment(v).format("MMM DD")}
            />
            <ChartTooltip
              content={
                <ChartTooltipContent
                  className="w-[150px] "
                  labelFormatter={(v) => moment(v).format("MMM DD, YYYY")}
                />
              }
            />
            <Line
              dataKey={activeChart}
              type="natural"
              stroke={`var(--color-${activeChart})`}
              strokeWidth={2}
              dot={{
                fill: "hsl(var(--background))",
                r: 3,
              }}
              activeDot={{
                r: 6,
              }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              domain={["auto", "auto"]}
            ></YAxis>
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}
