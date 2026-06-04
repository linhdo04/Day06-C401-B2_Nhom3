export type Priority = "price" | "time" | "pickup_distance";

export type TransportMode = "all" | "bus" | "train" | "flight";

export type PathType = "happy" | "low_confidence" | "failure" | "clarification";

export type ClarificationChoice = "pickup_place" | "bus_operator";

export type TripQuery = {
  from_city: string;
  to_city: string;
  date: string;
  duration_days: number;
  budget_vnd: number;
  travelers: number;
  pickup_text: string;
  user_location: {
    label: string;
    lat: number;
    lng: number;
  };
  priority: Priority;
  transport_mode: TransportMode;
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

export type WebSearchResult = {
  title: string;
  url: string;
  snippet: string;
  source: string;
};

export type CollectedTransportation = {
  transport_type: string;
  provider: string;
  price: number;
  departure: string;
  arrival: string;
  pickup: string;
  source: string;
};

export type CollectedHotel = {
  hotel_name: string;
  price_per_night: number;
  rating: number;
  distance_to_center: number;
};

export type FoodEstimate = {
  category: string;
  cost_per_day: number;
};

export type RankedPlanOption = {
  option: string;
  total_cost: number;
  comfort_score: number;
  speed_score: number;
  budget_fit: number;
  decision_reason: string;
};

export type ItineraryDay = {
  day: number;
  title: string;
  activities: string[];
  estimated_cost: number;
};

export type AgentResponse = {
  path: PathType;
  summary: string;
  tickets: TicketOption[];
  web_results: WebSearchResult[];
  transportation_data: CollectedTransportation[];
  hotels_data: CollectedHotel[];
  food_estimates: FoodEstimate[];
  ranked_plan_options: RankedPlanOption[];
  decision: string | null;
  itinerary: ItineraryDay[];
  warning: string | null;
  clarification_question: string | null;
  clarification_options: ClarificationChoice[];
  suggested_dates: string[];
};
