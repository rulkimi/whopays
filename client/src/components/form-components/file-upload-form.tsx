"use client";

import type { FieldPath, FieldValues, Control } from "react-hook-form";
import { FileUploader } from "@/components/file-uploader";
import { CommonFormField } from "./common-form-field";
import { cn } from "@/lib/utils";

type FileUploadConfig = {
  maxSize?: number;
  acceptedTypes?: string[];
  maxFiles?: number;
  onUpload?: (files: File[]) => Promise<void>;
  progresses?: Record<string, number>;
  // Removed index signature with any type
};

type FormFileUploadProps<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
> = {
  control: Control<TFieldValues>;
  name: TName;
  label?: string;
  description?: string;
  required?: boolean;
  config?: FileUploadConfig;
  disabled?: boolean;
  className?: string;
};

function FileUploadForm<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
>({
  control,
  name,
  label,
  description,
  required,
  config,
  disabled,
  className,
}: FormFileUploadProps<TFieldValues, TName>
) {
  const {
    maxSize,
    acceptedTypes,
    maxFiles = 1,
    ...restConfig
  } = config || {};

  // Helper type for the accept object
  type AcceptedTypesMap = Record<string, string[]>;

  return (
    <CommonFormField
      control={control}
      name={name}
      label={label}
      description={description}
      required={required}
      render={(field) => (
        <div className={cn("w-full min-w-0", className) }>
          <FileUploader
            value={field.value}
            onValueChange={field.onChange}
            accept={
              acceptedTypes?.reduce<AcceptedTypesMap>(
                (acc, type) => ({ ...acc, [type]: [] }),
                {}
              )
            }
            maxSize={maxSize}
            maxFiles={maxFiles}
            disabled={disabled}
            {...restConfig}
          />
        </div>
      )}
    />
  );
}

export { FileUploadForm, type FileUploadConfig };