"use client";

import { useState } from "react";
import { AlertCircle, Compass, Loader2, Route } from "lucide-react";

import { clarifyTickets, searchTickets } from "@/lib/api";
import type { AgentResponse, ClarificationChoice, Priority, TripQuery } from "@/lib/types";
import { ChatAssistant } from "@/components/ChatAssistant";
import { ResultsList } from "@/components/ResultsList";
import { SearchForm } from "@/components/SearchForm";

const defaultQuery: TripQuery = {
  from_city: "Ha Noi",
  to_city: "Da Nang",
  date: "2026-06-06",
  duration_days: 3,
  budget_vnd: 5000000,
  travelers: 2,
  pickup_text: "",
  user_location: {
    label: "Cau Giay, Hanoi",
    lat: 21.0369,
    lng: 105.7897
  },
  priority: "price",
  transport_mode: "bus"
};

function buildApiError(): AgentResponse {
  return {
    path: "failure",
    summary: "Chưa kết nối được Python backend.",
    tickets: [],
    web_results: [],
    transportation_data: [],
    hotels_data: [],
    food_estimates: [],
    ranked_plan_options: [],
    decision: null,
    itinerary: [],
    warning: "Hãy chạy `npm run backend` trước khi demo giao diện.",
    clarification_question: null,
    clarification_options: [],
    suggested_dates: []
  };
}

export default function Home() {
  const [query, setQuery] = useState<TripQuery>(defaultQuery);
  const [result, setResult] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  async function runSearch(nextQuery: TripQuery) {
    setLoading(true);
    setHasSearched(true);

    try {
      const response = await searchTickets(nextQuery);
      setResult(response);
    } catch {
      setResult(buildApiError());
    } finally {
      setLoading(false);
    }
  }

  async function handlePriorityChange(priority: Priority) {
    const nextQuery = { ...query, priority };
    setQuery(nextQuery);

    if (hasSearched) {
      await runSearch(nextQuery);
    }
  }

  async function handleClarify(choice: ClarificationChoice) {
    setLoading(true);

    try {
      const response = await clarifyTickets(query, choice);
      setResult(response);
    } catch {
      setResult(buildApiError());
    } finally {
      setLoading(false);
    }
  }

  async function handleSuggestedDate(date: string) {
    const nextQuery = { ...query, date };
    setQuery(nextQuery);
    await runSearch(nextQuery);
  }

  return (
    <main className="app-shell">
      <header className="topbar" aria-label="SmartTravel header">
        <div className="brand-mark" aria-hidden="true">
          <Compass size={24} />
        </div>
        <div>
          <p className="eyebrow">Travel & Hospitality · AI planning prototype</p>
          <h1>SmartTravel AI</h1>
        </div>
      </header>

      <section className="workspace" aria-label="SmartTravel search workspace">
        <aside className="search-pane">
          <div className="pane-heading">
            <Route aria-hidden="true" size={20} />
            <div>
              <h2>Tìm phương án di chuyển</h2>
              <p>AI gợi ý vé xe, tàu, máy bay theo giá, thời gian và điểm đón thuận tiện.</p>
            </div>
          </div>

          <SearchForm
            loading={loading}
            query={query}
            onQueryChange={setQuery}
            onPriorityChange={handlePriorityChange}
            onSubmit={runSearch}
          />
        </aside>

        <section className="result-pane" aria-label="SmartTravel ranked results">
          {loading ? (
            <div className="empty-state" data-testid="loading-state">
              <Loader2 aria-hidden="true" className="spin" size={28} />
              <h2>Đang chạy SmartTravel agent</h2>
              <p>Đang đọc tuyến, kiểm tra nguồn dữ liệu và gợi ý phương án phù hợp.</p>
            </div>
          ) : result ? (
            <ResultsList
              query={query}
              result={result}
              onClarify={handleClarify}
              onSuggestedDate={handleSuggestedDate}
            />
          ) : (
            <div className="empty-state" data-testid="empty-state">
              <AlertCircle aria-hidden="true" size={28} />
              <h2>Sẵn sàng lên kế hoạch chuyến đi</h2>
              <p>Tìm phương tiện di chuyển trước, rồi hỏi trợ lý về lịch trình, điểm chơi và đặt phòng.</p>
            </div>
          )}
        </section>
      </section>

      <ChatAssistant />
    </main>
  );
}
