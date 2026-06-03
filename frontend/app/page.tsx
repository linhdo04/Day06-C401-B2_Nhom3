"use client";

import { useState } from "react";
import { AlertCircle, BusFront, Loader2, Route } from "lucide-react";

import { clarifyTickets, searchTickets } from "@/lib/api";
import type { AgentResponse, ClarificationChoice, Priority, TripQuery } from "@/lib/types";
import { ChatAssistant } from "@/components/ChatAssistant";
import { ResultsList } from "@/components/ResultsList";
import { SearchForm } from "@/components/SearchForm";

const defaultQuery: TripQuery = {
  from_city: "",
  to_city: "",
  date: "",
  pickup_text: "",
  user_location: {
    label: "",
    lat: 0,
    lng: 0
  },
  priority: "pickup_distance"
};

function buildApiError(): AgentResponse {
  return {
    path: "failure",
    summary: "Chưa kết nối được Python backend.",
    tickets: [],
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
      <header className="topbar" aria-label="SmartBus header">
        <div className="brand-mark" aria-hidden="true">
          <BusFront size={24} />
        </div>
        <div>
          <p className="eyebrow">Travel & Hospitality · Day 06 prototype</p>
          <h1>SmartBus AI</h1>
        </div>
      </header>

      <section className="workspace" aria-label="SmartBus search workspace">
        <aside className="search-pane">
          <div className="pane-heading">
            <Route aria-hidden="true" size={20} />
            <div>
              <h2>Tìm vé liên tỉnh</h2>
              <p>AI xếp hạng theo giá, giờ đi và khoảng cách điểm đón.</p>
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

        <section className="result-pane" aria-label="SmartBus ranked results">
          {loading ? (
            <div className="empty-state" data-testid="loading-state">
              <Loader2 aria-hidden="true" className="spin" size={28} />
              <h2>Đang chạy agent Python</h2>
              <p>Đang tách intent, kiểm tra nhập nhằng và xếp hạng lựa chọn.</p>
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
              <h2>Sẵn sàng so sánh vé</h2>
              <p>Giữ dữ liệu mặc định để demo nhanh, hoặc đổi tuyến/ngày/điểm đón.</p>
            </div>
          )}
        </section>
      </section>

      <ChatAssistant />
    </main>
  );
}
