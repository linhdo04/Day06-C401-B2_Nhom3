import { NextRequest, NextResponse } from "next/server";
import type { AgentResponse } from "@/lib/types";

const BACKEND = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

const CLARIFY_RESPONSE: AgentResponse = {
  path: "clarification",
  summary: "Có nhiều điểm đón ở khu vực bạn chọn. Bạn muốn đón ở đâu?",
  warning: null,
  clarification_question: "Khu vực của bạn có nhiều điểm đón. Bạn muốn ưu tiên theo điều gì?",
  clarification_options: ["pickup_place", "bus_operator"],
  suggested_dates: [],
  tickets: []
};

export async function POST(req: NextRequest): Promise<NextResponse> {
  try {
    const res = await fetch(`${BACKEND}/api/clarify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: await req.text(),
      signal: AbortSignal.timeout(3000),
    });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {
    // backend unreachable — fall through to mock
  }

  await new Promise((r) => setTimeout(r, 600));
  return NextResponse.json(CLARIFY_RESPONSE);
}
