/**
 * Formats a number as a price string in Malaysian currency format.
 * For example: 1234.56 -> "RM 1,234.56"
 *
 * @param value - The number to format
 * @param options - Optional Intl.NumberFormat options override
 * @returns {string} Formatted price string
 */
export function formatPrice(
  value: number,
  options?: Intl.NumberFormatOptions
): string {
  if (typeof value !== "number" || isNaN(value)) return "RM 0.00";
  const formatter = new Intl.NumberFormat("en-MY", {
    style: "currency",
    currency: "MYR",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
    ...options,
  });

  // "RM 1,234.56" is the output, but for web, prefer "RM 1,234.56" (non-breaking space => normal space)
  return formatter
    .format(value)
    .replace(String.fromCharCode(160), " ");
}
