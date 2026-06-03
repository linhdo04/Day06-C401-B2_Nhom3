"use client";

import { useEffect, useRef, useState } from "react";
import { LocateFixed } from "lucide-react";

type NominatimResult = {
  display_name: string;
  lat: string;
  lon: string;
};

type UserLocation = {
  label: string;
  lat: number;
  lng: number;
};

type Props = {
  value: string;
  onChange: (text: string, coords?: UserLocation) => void;
  placeholder?: string;
};

export function LocationAutocomplete({ value, onChange, placeholder }: Props) {
  const [suggestions, setSuggestions] = useState<NominatimResult[]>([]);
  const [open, setOpen] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const wrapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onClickOutside(e: MouseEvent) {
      if (wrapRef.current && !wrapRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  function handleInput(text: string) {
    onChange(text);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (text.length < 3) {
      setSuggestions([]);
      setOpen(false);
      return;
    }
    debounceRef.current = setTimeout(async () => {
      try {
        const url =
          `https://nominatim.openstreetmap.org/search` +
          `?q=${encodeURIComponent(text)}&countrycodes=vn&format=json&limit=6`;
        const res = await fetch(url, { headers: { "Accept-Language": "vi" } });
        const data: NominatimResult[] = await res.json();
        setSuggestions(data);
        setOpen(data.length > 0);
      } catch {
        setSuggestions([]);
        setOpen(false);
      }
    }, 350);
  }

  function handleSelect(s: NominatimResult) {
    const label = s.display_name.split(",").slice(0, 3).join(",").trim();
    onChange(label, { label, lat: parseFloat(s.lat), lng: parseFloat(s.lon) });
    setSuggestions([]);
    setOpen(false);
  }

  return (
    <div className="autocomplete-wrap" ref={wrapRef}>
      <div className="input-wrap">
        <LocateFixed aria-hidden="true" size={18} />
        <input
          data-testid="pickup-text"
          value={value}
          onChange={(e) => handleInput(e.target.value)}
          placeholder={placeholder ?? "Nhập địa điểm"}
          autoComplete="off"
        />
      </div>
      {open && (
        <ul className="autocomplete-dropdown" role="listbox">
          {suggestions.map((s, i) => (
            <li
              key={i}
              className="autocomplete-option"
              role="option"
              aria-selected={false}
              onMouseDown={() => handleSelect(s)}
            >
              {s.display_name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
