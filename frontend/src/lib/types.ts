export interface Membership {
  id: string;
  organization_id: string;
  organization_name: string;
  status: "active" | "invited" | "suspended";
  role_names: string[];
  permissions: string[];
  location_ids: string[];
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  memberships: Membership[];
}

export interface AuthResponse {
  access: string;
  user: User;
}

