"use server"

import { ReceiptsListResponse } from "@/types/api-response"
import { getAccessToken } from "./session"
import { getErrorResponse } from "@/lib/error-message";

export const fetchReceiptsList = async (): Promise<ReceiptsListResponse> => {
  const token = await getAccessToken();
  const url = `${process.env.API_URL}/receipts`;

  try {
    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const data = await response.json();

    if (!data.success) return getErrorResponse(data.message);

    return data;
  } catch (error) {
    return getErrorResponse(error);
  }
}