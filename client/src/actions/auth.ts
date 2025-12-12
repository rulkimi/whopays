"use server";

import { LoginValues } from "@/app/(auth)/login/_components/login-form";
import { RegisterValues } from "@/app/(auth)/register/_components/register-form";
import { getErrorResponse } from "@/lib/error-message";
import { objectToFormData } from "@/lib/form-data";
import { setSession } from "./session";
import { UserLoggedInResponse, UserRegisteredResponse } from "@/types/api-response";

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

    if (!data.success) return getErrorResponse(data.message);

    return data;
  } catch (error) {
    return getErrorResponse(error);
  }
}


export const loginUser = async (values: LoginValues): Promise<UserLoggedInResponse> => {
  const url = `${process.env.API_URL}/auth/login`;
  const formData = objectToFormData(values);

  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (!data.success) return getErrorResponse(data.message);

    await setSession(data.data);
    return data;
  } catch (error) {
    return getErrorResponse(error);
  }
}