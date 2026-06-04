# Individual reflection — 2A202600769_NguyenDucKienTrung

## 1. Role
Frontend developer. Phụ trách giao diện tương tác chính giữa user và hệ thống AI.

## 2. Đóng góp cụ thể
- `SearchForm.tsx` — form nhập hành trình, ngày đi, số khách, ngân sách, phương tiện.
- `PriorityControl.tsx` — control cho phép user chọn ưu tiên xếp hạng (giá / giờ / điểm đón gần).
- `ChatAssistant.tsx` + `api/chat/route.ts` — chat assistant tích hợp AI trả lời theo context chuyến đi.

## 3. SPEC mạnh/yếu

**Mạnh nhất:** Thiết kế clarification path cho lỗi nhầm địa danh/nhà xe ("Thanh Phong"). Thay vì để AI đoán sai rồi user phát hiện sau, SPEC buộc hệ thống hỏi lại trước khi xếp hạng — giải quyết đúng failure mode nguy hiểm nhất của sản phẩm.

**Yếu nhất:** Priority control ở frontend chưa được nối rõ thành signal ranking ở backend ngay từ đầu. Việc `rank_tickets()` dùng priority như thế nào chưa được đặc tả cụ thể trong SPEC, dẫn đến phải căn chỉnh lại khi tích hợp.

## 4. Đóng góp khác
Workshop cá nhân test Vietnam Airlines NEO — 6 queries, phân loại 4 paths. Phát hiện hard failure: khi user đặt vé qua OTA muốn đổi tên, bot chỉ nói "liên hệ nơi mua vé" mà không có hotline, link hay bước tiếp theo. Finding này nhắc nhóm thiết kế failure panel và clarification panel đủ cụ thể, không để user bị kẹt.

## 5. Điều học được
Form không chỉ là input — nó là nơi user khai báo intent và priority. Nếu không thiết kế rõ từ đầu, backend không biết dùng signal đó để làm gì. Priority control phải được xem là một phần của AI pipeline, không chỉ là UI filter.

## 6. Nếu làm lại
Thiết kế low-confidence state ngay từ phía form: khi user nhập thông tin mơ hồ, UI nên có tín hiệu sớm thay vì chờ backend trả về clarification panel mới hiện. Giảm được một round-trip và giữ trust của user tốt hơn.

## 7. AI giúp gì / AI sai gì

**Giúp:** Dùng Claude để draft nhanh chat route handler và gợi ý cấu trúc API response cho ChatAssistant.

**Sai/mislead:** Gợi ý component structure quá phức tạp cho priority control — thêm state management không cần thiết cho scope prototype 1 ngày.
