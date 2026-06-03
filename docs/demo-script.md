# SmartBus AI Demo Script

## 0:00 - 0:30 · Problem

Người đi tỉnh phải mở Vexere, MoMo, Facebook hoặc gọi nhà xe để so sánh giá, giờ đi và điểm đón. Pain chính không phải thiếu vé, mà là thiếu một bước ra quyết định đáng tin.

## 0:30 - 1:20 · Happy Path

1. Chạy search mặc định: Hà Nội -> Đà Nẵng, ngày `2026-06-06`, điểm đón Cầu Giấy.
2. Giải thích backend Python gọi các tool: detect ambiguity, search mock tickets, rank tickets, build Maps link.
3. Chỉ ra top 3 card có giá, giờ, khoảng cách điểm đón, Maps và deep-link đặt vé.

## 1:20 - 2:00 · Correction Path

1. Đổi ưu tiên từ `Điểm đón gần` sang `Giá thấp`.
2. Result re-rank ngay, không nhập lại route.
3. Nhấn mạnh AI augment quyết định, user vẫn chọn vé cuối cùng.

## 2:00 - 2:40 · Failure + Low Confidence

1. Đổi điểm đến sang Huế để thấy case chỉ còn 1 lựa chọn và cảnh báo điểm đón xa.
2. Đổi điểm đến sang Nha Trang ngày `2026-06-06` để thấy failure và ngày gợi ý.

## 2:40 - 3:00 · NER Failure Mitigation

1. Nhập `Giáo xứ Thanh Phong`.
2. Agent hỏi lại: địa danh điểm đón hay nhà xe.
3. Chọn địa danh, hệ thống vẫn hiển thị cảnh báo phải kiểm tra địa chỉ và Maps trước khi đặt.
