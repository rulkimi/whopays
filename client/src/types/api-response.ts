import { AuthData, User } from "./data";

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  code?: number;
}

// auth
export type UserRegisteredResponse = ApiResponse<User>;
export type UserLoggedInResponse = ApiResponse<AuthData>;