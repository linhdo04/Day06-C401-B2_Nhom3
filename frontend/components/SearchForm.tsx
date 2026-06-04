"use client";

import { FormEvent } from "react";
import { BusFront, CalendarDays, MapPin, Plane, Search, Sparkles, TrainFront } from "lucide-react";
import type { LucideIcon } from "lucide-react";

import type { Priority, TransportMode, TripQuery } from "@/lib/types";
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

const transportOptions: Array<{
  value: TransportMode;
  label: string;
  icon: LucideIcon;
}> = [
  { value: "bus", label: "Xe", icon: BusFront },
  { value: "train", label: "Tàu", icon: TrainFront },
  { value: "flight", label: "Máy bay", icon: Plane },
  { value: "all", label: "Tất cả", icon: Sparkles }
];

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
          <span>Điểm đi</span>
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
          <span>Điểm đến</span>
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
        <span>Ngày khởi hành</span>
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
        <span>Điểm đón, ga, sân bay hoặc ghi chú vị trí</span>
        <LocationAutocomplete
          value={query.pickup_text}
          onChange={handlePickupChange}
          placeholder="Cầu Giấy, ga Hà Nội hoặc sân bay Nội Bài"
        />
      </label>

      <fieldset className="priority-control transport-control">
        <legend>Phương tiện</legend>
        <div className="segment-row" data-testid="transport-mode-control">
          {transportOptions.map((option) => {
            const Icon = option.icon;
            return (
              <button
                aria-pressed={query.transport_mode === option.value}
                className={query.transport_mode === option.value ? "segment active" : "segment"}
                data-testid={`transport-${option.value}`}
                key={option.value}
                onClick={() => updateField("transport_mode", option.value)}
                type="button"
              >
                <Icon aria-hidden={true} size={16} />
                <span>{option.label}</span>
              </button>
            );
          })}
        </div>
      </fieldset>

      <PriorityControl value={query.priority} onChange={onPriorityChange} />

      <button className="primary-action" data-testid="search-submit" type="submit" disabled={loading}>
        <Search aria-hidden="true" size={18} />
        <span>{loading ? "Đang tìm" : "Tìm phương án"}</span>
      </button>
    </form>
  );
}
