"use client";

import { FormEvent } from "react";
import { CalendarDays, MapPin, Search } from "lucide-react";

import type { Priority, TripQuery } from "@/lib/types";
import { VIETNAMESE_CITIES } from "@/lib/vietnamese-cities";
import { LocationAutocomplete } from "./LocationAutocomplete";
import { PriorityControl } from "./PriorityControl";

type SearchFormProps = {
  query: TripQuery;
  loading: boolean;
  onQueryChange: (query: TripQuery) => void;
  onPriorityChange: (priority: Priority) => void;
  onSubmit: (query: TripQuery) => void;
};

export function SearchForm({
  query,
  loading,
  onQueryChange,
  onPriorityChange,
  onSubmit
}: SearchFormProps) {
  function updateField(field: keyof TripQuery, value: string) {
    onQueryChange({ ...query, [field]: value });
  }

  function handlePickupChange(text: string, coords?: { label: string; lat: number; lng: number }) {
    onQueryChange({
      ...query,
      pickup_text: text,
      ...(coords ? { user_location: coords } : {})
    });
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit(query);
  }

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <datalist id="vn-cities">
        {VIETNAMESE_CITIES.map((city) => (
          <option key={city} value={city} />
        ))}
      </datalist>

      <div className="field-grid">
        <label>
          <span>Từ</span>
          <div className="input-wrap">
            <MapPin aria-hidden="true" size={18} />
            <input
              data-testid="from-city"
              list="vn-cities"
              value={query.from_city}
              onChange={(event) => updateField("from_city", event.target.value)}
              placeholder="Hà Nội"
              autoComplete="off"
            />
          </div>
        </label>

        <label>
          <span>Đến</span>
          <div className="input-wrap">
            <MapPin aria-hidden="true" size={18} />
            <input
              data-testid="to-city"
              list="vn-cities"
              value={query.to_city}
              onChange={(event) => updateField("to_city", event.target.value)}
              placeholder="Đà Nẵng"
              autoComplete="off"
            />
          </div>
        </label>
      </div>

      <label>
        <span>Ngày đi</span>
        <div className="input-wrap">
          <CalendarDays aria-hidden="true" size={18} />
          <input
            data-testid="date-input"
            type="date"
            value={query.date}
            onChange={(event) => updateField("date", event.target.value)}
          />
        </div>
      </label>

      <label>
        <span>Điểm đón hoặc ghi chú vị trí</span>
        <LocationAutocomplete
          value={query.pickup_text}
          onChange={handlePickupChange}
          placeholder="Cầu Giấy hoặc Giáo xứ Thanh Phong"
        />
      </label>

      <PriorityControl value={query.priority} onChange={onPriorityChange} />

      <button className="primary-action" data-testid="search-submit" type="submit" disabled={loading}>
        <Search aria-hidden="true" size={18} />
        <span>{loading ? "Đang tìm" : "Tìm vé phù hợp"}</span>
      </button>
    </form>
  );
}
