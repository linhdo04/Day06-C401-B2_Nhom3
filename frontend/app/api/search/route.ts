import { NextRequest, NextResponse } from "next/server";
import type { AgentResponse } from "@/lib/types";

const BACKEND = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

const MOCK_RESPONSE: AgentResponse = {
  path: "happy",
  summary: "Tìm thấy 3 chuyến xe phù hợp từ Hà Nội đến Đà Nẵng.",
  warning: null,
  clarification_question: null,
  clarification_options: [],
  suggested_dates: [],
  tickets: [
    {
      id: "ticket-001",
      provider: "vexere.com",
      operator: "Hoàng Long",
      from_city: "Hà Nội",
      to_city: "Đà Nẵng",
      date: "2026-06-06",
      departure_time: "06:00",
      arrival_time: "17:30",
      price_vnd: 350000,
      pickup_point: "Bến xe Mỹ Đình",
      pickup_address: "20 Phạm Hùng, Mỹ Đình, Nam Từ Liêm, Hà Nội",
      pickup_distance_km: 3.2,
      booking_url: "https://vexere.com",
      maps_url: "https://maps.google.com",
      rank_reason: "Giá rẻ nhất, điểm đón cách bạn 3.2 km."
    },
    {
      id: "ticket-002",
      provider: "vexere.com",
      operator: "Phương Trang",
      from_city: "Hà Nội",
      to_city: "Đà Nẵng",
      date: "2026-06-06",
      departure_time: "07:30",
      arrival_time: "19:00",
      price_vnd: 420000,
      pickup_point: "Bến xe Giáp Bát",
      pickup_address: "Nguyễn Xiển, Giáp Bát, Hoàng Mai, Hà Nội",
      pickup_distance_km: 7.8,
      booking_url: "https://vexere.com",
      maps_url: "https://maps.google.com",
      rank_reason: "Hãng uy tín, ghế giường nằm cao cấp."
    },
    {
      id: "ticket-003",
      provider: "baolau.vn",
      operator: "Thành Bưởi",
      from_city: "Hà Nội",
      to_city: "Đà Nẵng",
      date: "2026-06-06",
      departure_time: "19:00",
      arrival_time: "06:30",
      price_vnd: 390000,
      pickup_point: "Văn phòng Cầu Giấy",
      pickup_address: "144 Xuân Thủy, Cầu Giấy, Hà Nội",
      pickup_distance_km: 0.9,
      booking_url: "https://baolau.vn",
      maps_url: "https://maps.google.com",
      rank_reason: "Điểm đón gần nhất (0.9 km), xe giường nằm."
    }
  ]
};

export async function POST(req: NextRequest): Promise<NextResponse> {
  try {
    const res = await fetch(`${BACKEND}/api/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: await req.text(),
      signal: AbortSignal.timeout(3000),
    });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {
    // backend unreachable — fall through to mock
  }

  await new Promise((r) => setTimeout(r, 800));
  return NextResponse.json(MOCK_RESPONSE);
}
