"use client";

import * as React from "react";
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import type { DateRange } from "react-day-picker";
import type { FieldValues, FieldPath, Control } from "react-hook-form";
import { CommonFormField } from "./common-form-field"; // your base wrapper
import { useViewport } from "@/hooks/use-viewport";
import { cn } from "@/lib/utils";

interface DateRangeFormFieldProps<T extends FieldValues> {
	control: Control<T>;
	name: FieldPath<T>;
	label?: string;
	description?: string;
	required?: boolean;
	className?: string;
	placeholder?: string;
}

export function DateRangeFormField<T extends FieldValues>({
	control,
	name,
	label,
	description,
	required,
	className,
	placeholder = "Select date range",
}: DateRangeFormFieldProps<T>) {
	const viewport = useViewport();

	return (
		<CommonFormField
			control={control}
			name={name}
			label={label}
			description={description}
			required={required}
			render={({ value, onChange }) => {
				const dateRange = value as DateRange | undefined;

				return (
					<Popover>
						<PopoverTrigger asChild>
							<Button
								variant="outline"
								data-empty={!dateRange?.from || !dateRange?.to}
								className={cn(
									"data-[empty=true]:text-muted-foreground w-full justify-start text-left font-normal",
									className
								)}
							>
								<CalendarIcon className="mr-2 h-4 w-4 shrink-0" />
								{dateRange?.from && dateRange?.to ? (
									<span className="truncate">
										{format(dateRange.from, "MMM dd")} - {format(dateRange.to, "MMM dd, yyyy")}
									</span>
								) : (
									<span className="truncate">{placeholder}</span>
								)}
							</Button>
						</PopoverTrigger>

						<PopoverContent className="w-auto p-0" align="start">
							<Calendar
								mode="range"
								selected={dateRange}
								onSelect={onChange}
								numberOfMonths={viewport.width >= 768 ? 2 : 1}
							/>
						</PopoverContent>
					</Popover>
				);
			}}
		/>
	);
}
