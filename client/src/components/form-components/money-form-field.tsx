"use client";

import type { Control, FieldPath, FieldValues } from "react-hook-form";
import { CommonFormField } from "./common-form-field";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";

interface MoneyFormFieldProps<T extends FieldValues> {
  control: Control<T>;
  name: FieldPath<T>;
  label?: string;
  description?: string;
  required?: boolean;
  placeholder?: string;
  disabled?: boolean;
}

export function MoneyFormField<T extends FieldValues>({
  control,
  name,
  label,
  description,
  required,
  placeholder = "0.00",
  disabled,
}: MoneyFormFieldProps<T>) {
  return (
    <CommonFormField
      control={control}
      name={name}
      label={label}
      description={description}
      required={required}
      render={(field) => (
        <InputGroup>
          <InputGroupAddon align="inline-start">
            <span>RM</span>
          </InputGroupAddon>
          <InputGroupInput
            {...field}
            id={name}
            type="text"
            placeholder={placeholder}
            disabled={disabled}
            onChange={(e) => {
              const value = e.target.value.replace(/[^0-9.]/g, "");
              field.onChange(value);
            }}
          />
        </InputGroup>
      )}
    />
  );
}
