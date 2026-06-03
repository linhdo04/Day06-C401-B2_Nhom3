export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
    maximumFractionDigits: 0
  }).format(value);
}

export function priorityLabel(value: string): string {
  if (value === "pickup_distance") {
    return "Điểm đón gần";
  }

  if (value === "time") {
    return "Giờ đi";
  }

  return "Giá";
}
