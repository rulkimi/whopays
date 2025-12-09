import type { FieldValues, FieldPath, Control } from "react-hook-form";
import { useState } from "react";
import { CommonFormField } from "./common-form-field";
import {
  InputGroup,
  InputGroupInput,
  InputGroupButton
} from "../ui/input-group";
import { Button } from "../ui/button";

type MultipleDataInputFormFieldProps<T extends FieldValues> = {
  control: Control<T>;
  name: FieldPath<T>;
  label?: string;
  description?: string;
  required?: boolean;
  placeholder?: string;
  inputLabel?: string; // optional label next to Add Input
  itemLabel?: string; // label for each item
  disabled?: boolean;
};

export function MultipleDataInputFormField<T extends FieldValues>({
  control,
  name,
  label,
  description,
  required,
  placeholder = "",
  inputLabel,
  itemLabel,
  disabled,
}: MultipleDataInputFormFieldProps<T>) {
  // local state for the current input value before add
  const [currentValue, setCurrentValue] = useState("");

  return (
    <CommonFormField
      control={control}
      name={name}
      label={label}
      description={description}
      required={required}
      render={({ value = [], onChange }) => {

        // value is (string[] | undefined)
        const values: string[] = Array.isArray(value) ? value : [];

        // add to list if nonempty and unique
        const handleAdd = () => {
          const newVal = currentValue.trim();
          if (!newVal) return;
          if (values.includes(newVal)) {
            setCurrentValue(""); // clear anyway
            return;
          }
          onChange([...values, newVal]);
          setCurrentValue("");
        };

        const handleRemove = (idx: number) => {
          const next = values.filter((_, i) => i !== idx);
          onChange(next);
        };

        // Enter key shortcut
        const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
          if (e.key === "Enter") {
            e.preventDefault();
            handleAdd();
          }
        };

        return (
          <div>
            <InputGroup>
              <InputGroupInput
                value={currentValue}
                onChange={e => setCurrentValue(e.target.value)}
                placeholder={placeholder}
                aria-label={inputLabel}
                disabled={disabled}
                onKeyDown={handleInputKeyDown}
              />
              <InputGroupButton
                type="button"
                size="sm"
                onClick={handleAdd}
                disabled={disabled || !currentValue.trim()}
              >
                Add
              </InputGroupButton>
            </InputGroup>
            {/* List of added values */}
            <div className="mt-2 flex flex-col gap-2">
              {values.length > 0 ? values.map((val, idx) => (
                <div key={val} className="flex items-center">
                  <div className="flex-1 truncate" title={val}>
                    {itemLabel ? `${itemLabel}: ` : null}{val}
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon-sm"
                    aria-label="Remove"
                    onClick={() => handleRemove(idx)}
                    className="ml-2"
                  >
                    ×
                  </Button>
                </div>
              )) : (
                <div className="text-muted-foreground text-sm">No items added.</div>
              )}
            </div>
          </div>
        );
      }}
    />
  );
}
