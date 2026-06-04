import { ArrowUpRight, Globe2, SearchCheck } from "lucide-react";

import type { AgentResponse, TripQuery } from "@/lib/types";

type WebResultsPanelProps = {
  query: TripQuery;
  result: AgentResponse;
};

export function WebResultsPanel({ query, result }: WebResultsPanelProps) {
  return (
    <div className="results-stack">
      <div className="result-heading">
        <div>
          <p className="eyebrow">Nguồn tham khảo từ web</p>
          <h2>
            {query.from_city} → {query.to_city}
          </h2>
          <p className="result-note">Mở nguồn phù hợp để xem chi tiết giá, giờ đi, tình trạng chỗ và điều kiện đặt.</p>
        </div>
        <span className="date-chip">{query.date}</span>
      </div>

      <div className="web-result-list" data-testid="web-result-list">
        {result.web_results.map((source, index) => (
          <article className="web-result-card" data-testid="web-result-card" key={source.url}>
            <div className="ticket-rank" aria-label={`Nguồn ${index + 1}`}>
              {index + 1}
            </div>

            <div className="web-result-main">
              <div>
                <p className="provider">
                  <Globe2 aria-hidden="true" size={14} />
                  {source.source}
                </p>
                <h3>{source.title}</h3>
              </div>

              {source.snippet ? <p>{source.snippet}</p> : null}

              <a href={source.url} rel="noreferrer" target="_blank">
                <SearchCheck aria-hidden="true" size={16} />
                Mở nguồn
                <ArrowUpRight aria-hidden="true" size={14} />
              </a>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
