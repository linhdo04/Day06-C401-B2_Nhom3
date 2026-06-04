import type { AgentResponse, ClarificationChoice, TripQuery } from "./types";

async function postJson<TResponse>(path: string, body: unknown): Promise<TResponse> {
  const response = await fetch(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    throw new Error(`API ${path} failed with ${response.status}`);
  }

  return response.json() as Promise<TResponse>;
}

export function searchTickets(query: TripQuery): Promise<AgentResponse> {
  return postJson<AgentResponse>("/api/search", query);
}

export function clarifyTickets(
  query: TripQuery,
  choice: ClarificationChoice
): Promise<AgentResponse> {
  return postJson<AgentResponse>("/api/clarify", { query, choice });
}
