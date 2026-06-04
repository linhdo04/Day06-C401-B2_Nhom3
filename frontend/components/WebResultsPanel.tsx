import { ArrowUpRight, BedDouble, CalendarDays, CheckCircle2, Soup, TrainFront } from "lucide-react";

import type { AgentResponse, TripQuery } from "@/lib/types";
import { formatCurrency } from "@/lib/format";

type WebResultsPanelProps = {
  query: TripQuery;
  result: AgentResponse;
};

export function WebResultsPanel({ query, result }: WebResultsPanelProps) {
  return (
    <div className="results-stack">
      <div className="result-heading">
        <div>
          <p className="eyebrow">Planning Agent</p>
          <h2>
            {query.from_city} → {query.to_city}
          </h2>
          <p className="result-note">
            {query.duration_days} ngày · {query.travelers} khách · ngân sách {formatCurrency(query.budget_vnd)}
          </p>
        </div>
        <span className="date-chip">{query.date}</span>
      </div>

      <section className="planning-section" data-testid="data-collected-panel">
        <div className="section-title">
          <TrainFront aria-hidden="true" size={18} />
          <h3>Data Collected From Web</h3>
        </div>

        <div className="data-grid">
          <DataTable
            title="Transportation"
            rows={result.transportation_data.map((item) => [
              item.transport_type,
              item.provider,
              formatCurrency(item.price),
              item.departure
            ])}
            headers={["Type", "Provider", "Price", "Departure"]}
          />

          <DataTable
            title="Hotels"
            rows={result.hotels_data.map((item) => [
              item.hotel_name,
              formatCurrency(item.price_per_night),
              item.rating.toFixed(1),
              `${item.distance_to_center} km`
            ])}
            headers={["Hotel", "Night", "Rating", "Center"]}
          />

          <DataTable
            title="Food Estimate"
            rows={result.food_estimates.map((item) => [item.category, formatCurrency(item.cost_per_day)])}
            headers={["Category", "Cost/day"]}
          />
        </div>
      </section>

      <section className="planning-section" data-testid="ranking-panel">
        <div className="section-title">
          <CheckCircle2 aria-hidden="true" size={18} />
          <h3>Ranking Engine</h3>
        </div>

        <div className="ranking-list">
          {result.ranked_plan_options.map((option, index) => (
            <article className="ranking-card" key={option.option}>
              <div className="ticket-rank">{index + 1}</div>
              <div>
                <h3>{option.option}</h3>
                <p>{option.decision_reason}</p>
                <div className="score-row">
                  <span>{formatCurrency(option.total_cost)}</span>
                  <span>Comfort {option.comfort_score}/10</span>
                  <span>Speed {option.speed_score}/10</span>
                  <span>Budget {option.budget_fit}/10</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      {result.decision ? (
        <section className="decision-strip" data-testid="decision-panel">
          <CheckCircle2 aria-hidden="true" size={20} />
          <p>{result.decision}</p>
        </section>
      ) : null}

      <section className="planning-section" data-testid="itinerary-panel">
        <div className="section-title">
          <CalendarDays aria-hidden="true" size={18} />
          <h3>Generated Itinerary</h3>
        </div>

        <div className="itinerary-list">
          {result.itinerary.map((day) => (
            <article className="itinerary-day" key={day.day}>
              <div>
                <span>Day {day.day}</span>
                <h3>{day.title}</h3>
              </div>
              <ul>
                {day.activities.map((activity) => (
                  <li key={activity}>{activity}</li>
                ))}
              </ul>
              <p>{formatCurrency(day.estimated_cost)}</p>
            </article>
          ))}
        </div>
      </section>

      {result.web_results.length > 0 ? (
        <section className="planning-section">
          <div className="section-title">
            <Soup aria-hidden="true" size={18} />
            <h3>Web Sources</h3>
          </div>
          <div className="source-link-list">
            {result.web_results.map((source) => (
              <a href={source.url} key={source.url} rel="noreferrer" target="_blank">
                {source.title}
                <ArrowUpRight aria-hidden="true" size={14} />
              </a>
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}

function DataTable({
  title,
  headers,
  rows
}: {
  title: string;
  headers: string[];
  rows: string[][];
}) {
  return (
    <article className="data-table">
      <div className="data-table-title">
        <BedDouble aria-hidden="true" size={16} />
        <h3>{title}</h3>
      </div>
      <table>
        <thead>
          <tr>
            {headers.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={`${title}-${rowIndex}`}>
              {row.map((cell, cellIndex) => (
                <td key={`${title}-${rowIndex}-${cellIndex}`}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  );
}
