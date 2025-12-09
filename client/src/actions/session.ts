"use server"

import { AuthData } from "@/types/data";
import { SignJWT, jwtVerify } from "jose";
import { cookies } from "next/headers";

const SECRET_KEY = process.env.JWT_SECRET;
const encodedKey = new TextEncoder().encode(SECRET_KEY);

type DataToEncrypt = Omit<AuthData, "refresh_token" | "refresh_token_expiry">;

const encryptSession = async (data: DataToEncrypt) => {
  return new SignJWT(data)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("1h")
    .sign(encodedKey)
};

type DecryptedData = DataToEncrypt;

const decryptSession = async (token: string): Promise<DecryptedData | null> => {
  try {
    const { payload } = await jwtVerify(token, encodedKey);
    return payload as DecryptedData;
  } catch {
    return null;
  }
}

export const setSession = async (data: AuthData) => {
  const cookieStore = await cookies();

  const accessTokenExpiry = new Date(data.access_token_expiry);
  const accessTokenMaxAge = Math.max(
    0,
    Math.floor((accessTokenExpiry.getTime() -  Date.now()) / 1000)
  );

  const refreshTokenExpiry = new Date(data.refresh_token_expiry);
  const refreshTokenMaxAge = Math.max(
    0,
    Math.floor((refreshTokenExpiry.getTime() -  Date.now()) / 1000)
  );
  
  const sessionJWT = await encryptSession({
    user: data.user,
    access_token: data.access_token,
    access_token_expiry: data.access_token_expiry
  });

  cookieStore.set("session", sessionJWT, {
    httpOnly: true,
    secure: true,
    sameSite: "lax",
    path: "/",
    maxAge: accessTokenMaxAge
  });

  cookieStore.set("refresh", data.refresh_token, {
    httpOnly: true,
    secure: true,
    sameSite: "lax",
    path: "/",
    maxAge: refreshTokenMaxAge
  });
};

export const getSession = async (): Promise<DecryptedData | null> => {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get("session")?.value;
  if (!sessionCookie) return null;
  return decryptSession(sessionCookie);
}

export const clearSession = async () => {
  const cookieStore = await cookies();
  cookieStore.delete("session");
  cookieStore.delete("refresh");
}

const isTokenExpired = (expiry: string) => {
  return new Date(expiry).getTime() - Date.now() < 30 * 1000;
}

export const refreshAccessToken = async (): Promise<AuthData | null> => {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get("refresh")?.value;
  if (!refreshToken) return null;

  const url = `${process.env.API_URL}/auth/refresh`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ refresh_token: refreshToken })
    });

    if (!response.ok) return null;
    const data = await response.json();
    if (!data.success || !data.data) return null;

    await setSession(data.data);
    return data.data;
  } catch {
    return null
  }
}

export const getAccessToken = async (): Promise<string | null> => {
  const session = await getSession();

  if (!session) return null;

  if (isTokenExpired(session.access_token_expiry)) {
    const refreshed = await refreshAccessToken();
    if (!refreshed) {
      await clearSession();
      return null;
    }
    return refreshed.access_token;
  }
  return session.access_token;
}