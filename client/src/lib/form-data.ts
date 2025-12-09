import { base64ToFile } from "./file"

export type FormDataOptions<T> = {
  skipNull?: boolean
  stringify?: (keyof T)[]
  base64FileKeys?: (keyof T)[]
  array?: (keyof T)[]
  nullable?: (keyof T)[]
}
/**
 * Appends a value to FormData, handling Blob/File, arrays, and objects properly.
 */

function appendToFormData(
  formData: FormData,
  key: string,
  value: unknown,
) {
  if (value instanceof File || value instanceof Blob) {
    formData.append(key, value);
  } else if (Array.isArray(value)) {
    value.forEach((v, idx) => {
      appendToFormData(formData, `${key}[${idx}]`, v);
    });
  } else if (typeof value === "object" && value !== null) {
    // Avoid "[object File]" or "[object Object]" - flatten nested objects
    for (const [k, v] of Object.entries(value)) {
      appendToFormData(formData, `${key}[${k}]`, v);
    }
  } else if (typeof value === "boolean" || typeof value === "number" || typeof value === "string") {
    formData.append(key, String(value));
  } else {
  }
}

export function objectToFormData<T extends object>(
  obj: T,
  options: FormDataOptions<T> = {}
): FormData {
  const { skipNull = true, stringify = [], base64FileKeys = [], array = [], nullable = [] } = options;
  const formData = new FormData();

  (Object.keys(obj) as (keyof T)[]).forEach((key) => {
    const value = obj[key];

    // nullable: if string is "", send null
    let sendNullInstead = false;
    if (nullable.includes(key) && typeof value === "string" && value.trim() === "") {
      sendNullInstead = true;
    }

    if (skipNull && (value === undefined || value === null || sendNullInstead)) {
      return;
    }

    // At this point, if sendNullInstead, forcibly send null instead of the value
    if (sendNullInstead) {
      formData.append(String(key), "null");
      return;
    }

    // Remove all persisted-related handling for base64 files
    if (
      base64FileKeys.includes(key) &&
      typeof value === "object" &&
      value &&
      "base64" in value
    ) {
      const v = value as { base64: string; name?: string; type?: string };
      const mimeType = v.type;
      const fileName =
        (v && typeof v.name === "string" && v.name) ||
        `${String(key)}.jpg`;

      const file = base64ToFile(v.base64, fileName, mimeType);
      formData.append(String(key), file);
    } else if (array.includes(key) && Array.isArray(value)) {
      // Preferred: allergenIds[0]=2, allergenIds[1]=4, etc.
      value.forEach((item, idx) => {
        if (stringify.includes(key)) {
          formData.append(`${String(key)}[${idx}]`, String(item));
        } else if (item instanceof File || item instanceof Blob) {
          formData.append(`${String(key)}[${idx}]`, item);
        } else if (typeof item === "object" && item !== null) {
          // For nested objects in arrays, just JSON string
          formData.append(`${String(key)}[${idx}]`, JSON.stringify(item));
        } else {
          formData.append(`${String(key)}[${idx}]`, String(item));
        }
      });
    } else if (stringify.includes(key)) {
      // Explicitly stringify property per config
      formData.append(String(key), String(value));
    } else if (value instanceof File || value instanceof Blob) {
      // Native file instances: use as-is
      formData.append(String(key), value);
    } else if (Array.isArray(value)) {
      // Arrays not in "array" option sent as key[0], key[1], ...
      value.forEach((item, idx) => {
        if (stringify.includes(key)) {
          formData.append(`${String(key)}[${idx}]`, String(item));
        } else if (item instanceof File || item instanceof Blob) {
          formData.append(`${String(key)}[${idx}]`, item);
        } else if (typeof item === "object" && item !== null) {
          formData.append(`${String(key)}[${idx}]`, JSON.stringify(item));
        } else {
          formData.append(`${String(key)}[${idx}]`, String(item));
        }
      });
    } else if (typeof value === "object" && value !== null) {
      // For nested objects, flatten using appendToFormData
      appendToFormData(formData, String(key), value);
    } else if (typeof value === "boolean" || typeof value === "number" || typeof value === "string") {
      formData.append(String(key), String(value));
    }
  });

  return formData;
}