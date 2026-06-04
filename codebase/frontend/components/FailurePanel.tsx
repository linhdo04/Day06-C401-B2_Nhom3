import { CalendarPlus, SearchX } from "lucide-react";

import type { AgentResponse } from "@/lib/types";

type FailurePanelProps = {
  result: AgentResponse;
  onSuggestedDate: (date: string) => void;
};

export function FailurePanel({ result, onSuggestedDate }: FailurePanelProps) {
  return (
    <div className="decision-panel failure" data-testid="failure-panel">
      <div className="panel-icon">
        <SearchX aria-hidden="true" size={26} />
      </div>
      <p className="eyebrow">Không có vé đúng điều kiện</p>
      <h2>{result.summary}</h2>
      {result.warning ? <p>{result.warning}</p> : null}

      {result.suggested_dates.length ? (
        <div className="suggested-dates">
          <span>Ngày gần nhất có dữ liệu</span>
          <div>
            {result.suggested_dates.map((date) => (
              <button
                data-testid="suggested-date"
                key={date}
                onClick={() => onSuggestedDate(date)}
                type="button"
              >
                <CalendarPlus aria-hidden="true" size={16} />
                {date}
              </button>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}
