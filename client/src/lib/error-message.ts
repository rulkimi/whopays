import { ApiResponse } from "@/types/api-response";

function getFriendlyErrorMessage(message: string | undefined): string {
  if (!message) {
    return "Sorry, we couldn't load the data. Please try again later.";
  }
  const lowerMsg = message.toLowerCase();
  if (
    lowerMsg.includes("fetch failed") ||
    lowerMsg.includes("network error") ||
    lowerMsg.includes("failed to fetch") ||
    lowerMsg.includes("network request failed")
  ) {
    return "Sorry, we couldn't connect to the server. Please check your internet connection and try again.";
  }
  return message;
}

export function getErrorResponse<T>(error: unknown): ApiResponse<T> {
  let message: string;
  let errors: Record<string, string>[] | undefined = undefined;

  if (
    Array.isArray(error) &&
    error.every(
      (item) =>
        typeof item === "object" && item !== null && !Array.isArray(item)
    )
  ) {
    // error is an array of Record<string, string>
    errors = error as Record<string, string>[];
    message = "Validation failed. Please check the errors below.";
  } else if (
    typeof error === "object" &&
    error !== null &&
    !Array.isArray(error)
  ) {
    // error is an object like { phone_number: 'Phone number already registered' }
    const errorObject = error as Record<string, string>;
    errors = [errorObject];
    // Get the first error message or default
    const firstErrorMsg = Object.values(errorObject)[0];
    message =
      firstErrorMsg ??
      "Validation failed. Please check the errors below.";
  } else if (error instanceof Error) {
    message = getFriendlyErrorMessage(error.message);
  } else if (typeof error === "string") {
    message = getFriendlyErrorMessage(error);
  } else {
    message = "An unexpected error occurred. Please try again later.";
  }

  return {
    success: false,
    message,
    data: undefined as unknown as T,
    ...(errors ? { errors } : {}),
  };
}

export function getPageErrorMessage(response?: {
  success?: boolean;
  message?: string;
}) {
  if (!response?.success) {
    return (
      getFriendlyErrorMessage(response?.message) ||
      "Sorry, we couldn't load the chalets. Please try again later."
    );
  }
  return undefined;
}
