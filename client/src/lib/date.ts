/**
 * Formats a date as "25 Jan 2025".
 * 
 * @param date - Date object or valid date input.
 * @returns {string} Formatted date string.
 */
export function formatDate(date: Date | string | number): string {
  const d = date instanceof Date ? date : new Date(date);
  if (isNaN(d.getTime())) return "";
  const day = d.getDate();
  const monthShort = d.toLocaleString("en-US", { month: "short" });
  const year = d.getFullYear();
  return `${day} ${monthShort} ${year}`;
}

