"use client";

import { X as IconX, Upload as IconUpload } from "lucide-react";
import Image from "next/image";
import * as React from "react";
import Dropzone, { type DropzoneProps } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { cn, formatBytes } from "@/lib/utils";

type FileWithPreview = File & { preview?: string };

export interface FileUploaderProps {
  value?: File | File[];
  onValueChange?: (val: File | File[] | null) => void;
  accept?: DropzoneProps["accept"];
  maxSize?: number;
  maxFiles?: number;
  disabled?: boolean;
}

export function FileUploader(props: FileUploaderProps) {
  const {
    value,
    onValueChange,
    accept = { "image/*": [] },
    maxSize = 2 * 1024 * 1024,
    maxFiles = 1,
    disabled = false,
  } = props;

  const filesArray = Array.isArray(value)
    ? value
    : value
    ? [value]
    : [];

  const [files, setFiles] = React.useState<FileWithPreview[]>(filesArray);

  React.useEffect(() => {
    if (onValueChange) {
      if (maxFiles === 1) onValueChange(files[0] || null);
      else onValueChange(files);
    }
  }, [files, onValueChange, maxFiles]);

  const onDrop = (accepted: File[]) => {
    let filesToSet: FileWithPreview[] = accepted.map((file) =>
      Object.assign(file, { preview: URL.createObjectURL(file) })
    );
    if (maxFiles === 1) filesToSet = [filesToSet[0]];
    setFiles(filesToSet);
  };

  const removeFile = (idx: number) => {
    setFiles((old) => {
      const updated = old.slice();
      updated.splice(idx, 1);
      return updated;
    });
  };

  React.useEffect(() => {
    // Clean up previews on unmount or files change
    return () => {
      files.forEach((file) => {
        if (file.preview) URL.revokeObjectURL(file.preview);
      });
    };
  }, [files]);

  return (
    <div className="flex flex-col gap-2 w-full">
      <Dropzone
        onDrop={onDrop}
        accept={accept}
        maxSize={maxSize}
        maxFiles={maxFiles}
        multiple={maxFiles > 1}
        disabled={disabled}
      >
        {({ getRootProps, getInputProps }) => (
          <div
            {...getRootProps()}
            className={cn(
              "flex items-center border-2 border-dashed rounded-md p-4 bg-muted cursor-pointer transition",
              disabled && "pointer-events-none opacity-50"
            )}
          >
            <input {...getInputProps()} />
            <IconUpload className="mr-2" />
            <span>
              {maxFiles === 1
                ? "Click or drag to upload a file"
                : `Click or drag to upload up to ${maxFiles} files`}
            </span>
            <span className="ml-auto text-xs text-muted-foreground">
              Max size: {formatBytes(maxSize)}
            </span>
          </div>
        )}
      </Dropzone>

      <div>
        {files.length > 0 &&
          files.map((file, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between bg-muted rounded-md px-2 py-1 mt-2"
            >
              {file.type.startsWith("image/") && file.preview ? (
                <Image
                  src={file.preview}
                  alt={file.name}
                  width={32}
                  height={32}
                  className="rounded mr-2"
                />
              ) : (
                <div className="w-8 h-8 flex items-center justify-center bg-background rounded mr-2">
                  <span className="text-[10px] text-muted-foreground">No preview</span>
                </div>
              )}
              <span className="flex-1 truncate mx-2">{file.name}</span>
              <span className="text-xs text-muted-foreground mr-2">{formatBytes(file.size)}</span>
              <Button
                type="button"
                variant="ghost"
                size="icon"
                onClick={() => removeFile(idx)}
                className="ml-2"
              >
                <IconX className="h-4 w-4" />
              </Button>
            </div>
          ))}
      </div>
    </div>
  );
}