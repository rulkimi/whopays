import { useState } from "react";
import type {
  Control,
  FieldPath,
  FieldValues,
} from "react-hook-form";
import { InputGroup, InputGroupButton, InputGroupInput } from "../ui/input-group";
import { CommonFormField } from "./common-form-field";
import { Eye, EyeOff } from "lucide-react";

export function PasswordFormField<T extends FieldValues>({
  control,
  name,
  label = "Password",
  description,
  required,
  placeholder,
  disabled,
}: {
  control: Control<T>;
  name: FieldPath<T>;
  label?: string;
  description?: string;
  required?: boolean;
  placeholder?: string;
  disabled?: boolean;
}) {
  const [show, setShow] = useState(false);

  return (
    <CommonFormField
      control={control}
      name={name}
      label={label}
      description={description}
      required={required}
      render={(field) => (
        <InputGroup>
          <InputGroupInput
            {...field}
            type={show ? "text" : "password"}
            placeholder={placeholder}
            disabled={disabled}
            autoComplete="off"
            id={name}
          />
          <InputGroupButton
            type="button"
            tabIndex={-1}
            onClick={() => setShow((v) => !v)}
            aria-label={show ? "Hide password" : "Show password"}
          >
            {show ? <EyeOff className="size-4" /> : <Eye className="size-4" />}
          </InputGroupButton>
        </InputGroup>
      )}
    />
  );
}


