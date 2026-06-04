"use client";

import type { AgentResponse, ClarificationChoice, TripQuery } from "@/lib/types";
import { ClarificationPanel } from "./ClarificationPanel";
import { FailurePanel } from "./FailurePanel";
import { PathStatus } from "./PathStatus";
import { TicketCard } from "./TicketCard";
import { WebResultsPanel } from "./WebResultsPanel";

type ResultsListProps = {
  query: TripQuery;
  result: AgentResponse;
  onClarify: (choice: ClarificationChoice) => void;
  onSuggestedDate: (date: string) => void;
};

export function ResultsList({ query, result, onClarify, onSuggestedDate }: ResultsListProps) {
  if (result.path === "clarification") {
    return <ClarificationPanel result={result} onClarify={onClarify} />;
  }

  if (result.path === "failure") {
    return <FailurePanel result={result} onSuggestedDate={onSuggestedDate} />;
  }

  if (result.web_results.length > 0 && result.tickets.length === 0) {
    return <WebResultsPanel query={query} result={result} />;
  }

  return (
    <div className="results-stack">
      <PathStatus result={result} />

      <div className="result-heading">
        <div>
          <p className="eyebrow">Top {result.tickets.length} lựa chọn</p>
          <h2>
            {query.from_city} → {query.to_city}
          </h2>
        </div>
        <span className="date-chip">{query.date}</span>
      </div>

      <div className="ticket-list" data-testid="ticket-list">
        {result.tickets.map((ticket, index) => (
          <TicketCard key={ticket.id} rank={index + 1} ticket={ticket} />
        ))}
      </div>
    </div>
  );
}
