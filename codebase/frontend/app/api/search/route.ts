import { NextRequest, NextResponse } from "next/server";

const BACKEND = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";
const BACKEND_TIMEOUT_MS = 15000;

export async function POST(req: NextRequest): Promise<NextResponse> {
  try {
    const res = await fetch(`${BACKEND}/api/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: await req.text(),
      signal: AbortSignal.timeout(BACKEND_TIMEOUT_MS),
    });
    if (res.ok) return NextResponse.json(await res.json());
    const text = await res.text();
    console.error("[api/search] backend error", res.status, text);
    return NextResponse.json(
      { error: `Backend search lỗi ${res.status}. Kiểm tra log FastAPI để xem trace.` },
      { status: res.status }
    );
  } catch (error) {
    console.error("[api/search] backend unreachable", error);
    return NextResponse.json(
      { error: "Chưa kết nối được Python backend tại http://127.0.0.1:8000." },
      { status: 502 }
    );
  }
}
