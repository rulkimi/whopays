"use server";

import { RegisterValues } from "@/app/(auth)/register/_components/register-form";
import { getErrorResponse } from "@/lib/error-message";
import { objectToFormData } from "@/lib/form-data";
import { UserRegisteredResponse } from "@/types/api-response";

export const registerUser = async (values: RegisterValues): Promise<UserRegisteredResponse> => {
  const url = `${process.env.API_URL}/auth/register`;
  const formData = objectToFormData(values, {
    base64FileKeys: ["profile_photo"]
  });
  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData
    });

    
    const data = await response.json();
    console.log(data, formData)

    if (!data.success) return getErrorResponse(data.message);

    return data;
  } catch (error) {
    return getErrorResponse(error);
  }
}