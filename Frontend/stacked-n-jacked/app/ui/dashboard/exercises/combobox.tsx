"use client";

import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

export function TargetMusclesCombobox({
  targetMuscles,
  selectedMuscles,
  handleMuscleClick,
}: {
  targetMuscles: string[];
  selectedMuscles: string[];
  handleMuscleClick: (muscle: string) => void;
}) {
  const [value, setValue] = React.useState("");

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className="w-[200px] justify-between"
        >
          {value
            ? targetMuscles.find((muscle) => muscle === value)
            : "Select muscle..."}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search muscle..." />
          <CommandList>
            <CommandEmpty>No muscle found.</CommandEmpty>
            <CommandGroup>
              {targetMuscles.map((muscle) => (
                <CommandItem
                  key={muscle}
                  value={muscle}
                  onSelect={() => {
                    handleMuscleClick(muscle);
                    console.log(selectedMuscles);
                    setValue(selectedMuscles.length - 1 === 0 ? "" : muscle); //why tf length is alwyas "1 update" behind???
                  }}
                  //TODO TO FIX selectedMuscle is not current state
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      selectedMuscles.includes(muscle)
                        ? "opacity-100"
                        : "opacity-0"
                    )}
                  />
                  {muscle}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
