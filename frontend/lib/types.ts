export type Priority = "price" | "time" | "pickup_distance";

export type PathType = "happy" | "low_confidence" | "failure" | "clarification";

export type ClarificationChoice = "pickup_place" | "bus_operator";

export type TripQuery = {
  from_city: string;
  to_city: string;
  date: string;
  pickup_text: string;
  user_location: {
    label: string;
    lat: number;
    lng: number;
  };
  priority: Priority;
};

export type TicketOption = {
  id: string;
  provider: string;
  operator: string;
  from_city: string;
  to_city: string;
  date: string;
  departure_time: string;
  arrival_time: string;
  price_vnd: number;
  pickup_point: string;
  pickup_address: string;
  pickup_distance_km: number;
  booking_url: string;
  maps_url: string;
  rank_reason: string;
};

export type AgentResponse = {
  path: PathType;
  summary: string;
  tickets: TicketOption[];
  warning: string | null;
  clarification_question: string | null;
  clarification_options: ClarificationChoice[];
  suggested_dates: string[];
};
