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

  if (result.transportation_data.length > 0) {
    return (
      <div className="results-stack">
        <PathStatus result={result} />
        <WebResultsPanel query={query} result={result} />

        {result.tickets.length > 0 ? (
          <section className="planning-section">
            <div className="result-heading">
              <div>
                <p className="eyebrow">Normalized Ticket Options</p>
                <h2>Chi tiết phương tiện có thể đặt</h2>
              </div>
            </div>

            <div className="ticket-list" data-testid="ticket-list">
              {result.tickets.map((ticket, index) => (
                <TicketCard key={ticket.id} rank={index + 1} ticket={ticket} />
              ))}
            </div>
          </section>
        ) : null}
      </div>
    );
  }

  return (
    <div className="results-stack">
      <PathStatus result={result} />

      <div className="result-heading">
        <div>
          <p className="eyebrow">Top {result.tickets.length} phương án</p>
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
