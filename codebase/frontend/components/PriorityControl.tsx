"use client";

import { BadgeDollarSign, Clock, MapPinned } from "lucide-react";
import type { LucideIcon } from "lucide-react";

import type { Priority } from "@/lib/types";

type PriorityControlProps = {
  value: Priority;
  onChange: (priority: Priority) => void;
};

const options: Array<{
  value: Priority;
  label: string;
  icon: LucideIcon;
}> = [
  { value: "pickup_distance", label: "Vị trí tiện", icon: MapPinned },
  { value: "price", label: "Giá tốt", icon: BadgeDollarSign },
  { value: "time", label: "Giờ đi", icon: Clock }
];

export function PriorityControl({ value, onChange }: PriorityControlProps) {
  return (
    <fieldset className="priority-control">
      <legend>Ưu tiên gợi ý</legend>
      <div className="segment-row" data-testid="priority-control">
        {options.map((option) => {
          const Icon = option.icon;
          return (
            <button
              aria-pressed={value === option.value}
              className={value === option.value ? "segment active" : "segment"}
              data-testid={`priority-${option.value}`}
              key={option.value}
              onClick={() => onChange(option.value)}
              type="button"
            >
              <Icon aria-hidden={true} size={16} />
              <span>{option.label}</span>
            </button>
          );
        })}
      </div>
    </fieldset>
  );
}
