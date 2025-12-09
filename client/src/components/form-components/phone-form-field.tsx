"use client";

import type { Control, FieldPath, FieldValues } from "react-hook-form";
import { CommonFormField } from "./common-form-field";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";

interface PhoneFormFieldProps<T extends FieldValues> {
  control: Control<T>;
  name: FieldPath<T>;
  label?: string;
  description?: string;
  required?: boolean;
  placeholder?: string;
  disabled?: boolean;
}

export function PhoneFormField<T extends FieldValues>({
  control,
  name,
  label,
  description,
  required,
  placeholder,
  disabled,
}: PhoneFormFieldProps<T>) {
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
            <span>+60</span>
          </InputGroupAddon>
          <InputGroupInput
            {...field}
            id={name}
            type="text"
            placeholder={placeholder}
            disabled={disabled}
            onChange={(e) => {
              const value = e.target.value.replace(/[^0-9]/g, "");
              field.onChange(value);
            }}
          />
        </InputGroup>
      )}
    />
  );
}
