export type User = {
  username: string;
  name: string;
  email: string;
  id: string;
  photo_url: string;
};

export interface AuthData {
  user: User;
  access_token: string;
  access_token_expiry: string;
  refresh_token: string;
  refresh_token_expiry: string;
}
