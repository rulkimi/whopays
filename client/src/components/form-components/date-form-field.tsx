"use client";

import * as React from "react";
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import type { FieldValues, FieldPath, Control } from "react-hook-form";
import { CommonFormField } from "./common-form-field";
import { cn } from "@/lib/utils";

interface DateFormFieldProps<T extends FieldValues> {
  control: Control<T>;
  name: FieldPath<T>;
  label?: string;
  description?: string;
  required?: boolean;
  className?: string;
  placeholder?: string;
  disabled?: boolean;
}

export function DateFormField<T extends FieldValues>({
  control,
  name,
  label,
  description,
  required,
  className,
  placeholder = "Select date",
  disabled,
}: DateFormFieldProps<T>) {
  return (
    <CommonFormField
      control={control}
      name={name}
      label={label}
      description={description}
      required={required}
      render={({ value, onChange }) => {
        const date = value as Date | undefined;

        return (
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                data-empty={!date}
                disabled={disabled}
                className={cn(
                  "data-[empty=true]:text-muted-foreground w-full justify-start text-left font-normal",
                  className
                )}
              >
                <CalendarIcon className="mr-2 h-4 w-4 flex-shrink-0" />
                {date ? (
                  <span className="truncate">
                    {format(date, "MMM dd, yyyy")}
                  </span>
                ) : (
                  <span className="truncate">{placeholder}</span>
                )}
              </Button>
            </PopoverTrigger>

            <PopoverContent className="w-auto p-0" align="start">
              <Calendar mode="single" selected={date} onSelect={onChange} />
            </PopoverContent>
          </Popover>
        );
      }}
    />
  );
}
