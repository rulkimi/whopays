"use client";

import { useState } from "react";
import type { Control, ControllerRenderProps, FieldPath, FieldValues } from "react-hook-form";
import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
	Popover,
	PopoverTrigger,
	PopoverContent,
} from "@/components/ui/popover";
import {
	Command,
	CommandEmpty,
	CommandGroup,
	CommandInput,
	CommandItem,
	CommandList,
} from "@/components/ui/command";

import { CommonFormField } from "./common-form-field";

interface ConfigItem {
  id: string;
  name: string;
}
/* -------------------------------------------------------------------------- */
/*                                Type Helpers                                */
/* -------------------------------------------------------------------------- */

interface SelectFormFieldProps<T extends FieldValues> {
	control: Control<T>;
	name: FieldPath<T>;
	label?: string;
	description?: string;
	required?: boolean;
	options: ConfigItem[];
	placeholder?: string;
	searchPlaceholder?: string;
	emptyText?: string;
	width?: string;
}

/* -------------------------------------------------------------------------- */
/*                          Inner Select Renderer                             */
/* -------------------------------------------------------------------------- */

function SelectInner<T extends FieldValues>({
	field,
	options,
	placeholder,
	searchPlaceholder,
	emptyText,
	width,
	disabled = false,
}: {
	field: ControllerRenderProps<T, FieldPath<T>>;
	options: ConfigItem[];
	placeholder: string;
	searchPlaceholder: string;
	emptyText: string;
	width: string;
	disabled?: boolean;
}) {
	const [open, setOpen] = useState(false);
	const selected = options.find((opt) => opt.id === field.value);

	return (
		<Popover open={open} onOpenChange={setOpen} modal={true}>
			<PopoverTrigger asChild>
				<Button
					variant="outline"
					role="combobox"
					className={cn(`${width} text-foreground justify-between`)}
					disabled={disabled}
					aria-disabled={disabled}
					tabIndex={disabled ? -1 : undefined}
				>
					{selected ? selected.name : placeholder}
					<ChevronsUpDown className="opacity-50" />
				</Button>
			</PopoverTrigger>
			<PopoverContent
				className="p-0"
				style={{ width: "var(--radix-popover-trigger-width)" }}
			>
				<Command>
					<CommandInput placeholder={searchPlaceholder} className="h-9" disabled={disabled} />
					<CommandList>
						<CommandEmpty>{emptyText}</CommandEmpty>
						<CommandGroup>
							{options.map((opt) => (
								<CommandItem
									key={opt.id}
									value={opt.name}
									onSelect={() => {
										if (!disabled) {
											field.onChange(opt.id);
											setOpen(false);
										}
									}}
									aria-disabled={disabled}
									disabled={disabled}
									tabIndex={disabled ? -1 : undefined}
								>
									{opt.name}
									<Check
										className={cn(
											"ml-auto",
											opt.id === field.value
												? "opacity-100"
												: "opacity-0"
										)}
									/>
								</CommandItem>
							))}
						</CommandGroup>
					</CommandList>
				</Command>
			</PopoverContent>
		</Popover>
	);
}

/* -------------------------------------------------------------------------- */
/*                          Exported Form Field Wrapper                       */
/* -------------------------------------------------------------------------- */

export function SelectFormField<T extends FieldValues>({
	control,
	name,
	label,
	description,
	required,
	options,
	placeholder = "Select an option",
	searchPlaceholder = "Search...",
	emptyText = "No results found.",
	width = "w-full",
	disabled = false, // <-- added disabled prop with default to false
}: SelectFormFieldProps<T> & { disabled?: boolean }) {
	return (
		<CommonFormField
			control={control}
			name={name}
			label={label}
			description={description}
			required={required}
			render={(field) => (
				<SelectInner
					field={field}
					options={options}
					placeholder={placeholder}
					searchPlaceholder={searchPlaceholder}
					emptyText={emptyText}
					width={width}
					disabled={disabled} // <-- pass disabled prop
				/>
			)}
		/>
	);
}
