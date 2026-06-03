import { NextRequest, NextResponse } from "next/server";

const BACKEND = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

const MOCK_REPLIES: [RegExp, string][] = [
  [/giá|rẻ|price/i, "Giá vé thường dao động từ 150.000 – 500.000 VNĐ tùy tuyến và hãng xe. Bạn có thể chọn ưu tiên 'Giá thấp nhất' để SmartBus xếp hạng theo giá."],
  [/giờ|time|sớm|muộn/i, "Bạn muốn đi sớm hay tối? Chọn ưu tiên 'Giờ đi sớm nhất' và SmartBus sẽ hiển thị các chuyến sớm nhất trong ngày."],
  [/đón|điểm đón|pickup/i, "Nhập địa điểm đón của bạn vào ô 'Điểm đón', SmartBus sẽ tính khoảng cách từ bạn đến từng điểm đón và xếp hạng theo gần nhất."],
  [/tuyến|từ|đến|route/i, "Bạn có thể chọn tỉnh/thành phố từ danh sách gợi ý trong ô 'Từ' và 'Đến'. SmartBus hỗ trợ 63 tỉnh thành trên toàn quốc."],
  [/đặt|book|mua/i, "Sau khi tìm được vé phù hợp, bấm 'Đặt vé' trên thẻ kết quả để chuyển đến trang đặt vé của nhà cung cấp."],
];

function mockReply(message: string): string {
  for (const [pattern, reply] of MOCK_REPLIES) {
    if (pattern.test(message)) return reply;
  }
  return "Tôi hiểu câu hỏi của bạn. Hãy thử tìm kiếm với thông tin tuyến đường, ngày đi và điểm đón để SmartBus gợi ý vé phù hợp nhất cho bạn!";
}

export async function POST(req: NextRequest): Promise<NextResponse> {
  const body = await req.text();

  try {
    const res = await fetch(`${BACKEND}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
      signal: AbortSignal.timeout(3000),
    });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {
    // backend unreachable — fall through to mock
  }

  const { message } = JSON.parse(body) as { message: string };
  await new Promise((r) => setTimeout(r, 600));
  return NextResponse.json({ reply: mockReply(message) });
}
