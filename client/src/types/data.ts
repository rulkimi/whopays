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

export type ReceiptVariation = {
  name: string;
  price: number;
  id: string;
};

export type ReceiptParticipant = {
  id: string;
  is_owner: boolean;
  owes_amount: number | null;
  split_method: "equal" | "weighted";
  participant_type: "user" | "external";
  user_id: string | null;
  external_contact_id: string | null;
  user: User | null;
};

export type ReceiptItemFriend = {
  id: string;
  share_ratio: number | null;
  user_id: string | null;
  external_contact_id: string | null;
  user: User | null;
  // external_contact?: ExternalContact | null; // Uncomment if ExternalContact is defined
};

export type ReceiptItem = {
  name: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  id: string;
  variations: ReceiptVariation[];
  participants: ReceiptItemFriend[];
};

export type Receipt = {
  restaurant_name: string;
  subtotal: number;
  tax: number | null;
  service_charge: number | null;
  tip: number | null;
  rounding_amount: number | null;
  discount: number | null;
  total_amount: number;
  receipt_url: string | null;
  notes: string | null;
  status: string;
  id: string;
  user_id: string;
  participants: ReceiptParticipant[];
  items: ReceiptItem[];
  created_at: string;
  updated_at: string;
};

export type GetReceiptsResponse = {
  success: boolean;
  message: string;
  data: Receipt[];
  code: number;
};
