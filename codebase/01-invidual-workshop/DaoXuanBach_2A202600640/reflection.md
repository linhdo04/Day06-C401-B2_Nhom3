# Individual reflection — 2A202600640_Đào Xuân Bách

## 1. Role

Backend/frontend base developer. Phụ trách dựng khung kết nối giữa FastAPI backend và Next.js frontend, sửa lỗi tích hợp, và chuyển ý tưởng SmartTravel AI từ SPEC thành luồng demo chạy được.

## 2. Đóng góp cụ thể

- `backend/app/main.py` — thiết lập FastAPI app, CORS cho frontend local, health check và các API route chính: `/api/search`, `/api/clarify`, `/api/chat`.
- Kết nối backend service với schema response để frontend nhận cùng một cấu trúc dữ liệu cho happy path, low-confidence, failure và clarification.
- `frontend/app/page.tsx` — dựng page shell chính của SmartTravel AI, quản lý state query/result/loading, gọi API tìm kiếm, clarify và đổi ngày gợi ý.
- Tạo fallback UI khi frontend chưa kết nối được Python backend, giúp demo không bị trắng màn hình mà vẫn báo lỗi rõ ràng.
- Hỗ trợ bug fix trong quá trình tích hợp để form, kết quả, warning và chat assistant chạy chung trong một workflow.

## 3. SPEC mạnh/yếu

**Mạnh nhất:** SPEC đã mô tả được sản phẩm như một công cụ hỗ trợ ra quyết định, không chỉ là form tìm vé. Điều này giúp phần frontend-backend base có hướng rõ: API không chỉ trả danh sách vé, mà còn cần trả path, warning, decision, itinerary, link đặt vé và câu hỏi clarification.

**Yếu nhất:** Một số phần SPEC còn mở rộng nhanh từ SmartBus sang SmartTravel nên trong lúc build phải căn chỉnh lại tên gọi, data shape và UI copy. Nếu SPEC chốt sớm hơn về phạm vi dữ liệu nào là mock, dữ liệu nào là estimate, việc nối backend với frontend sẽ ít phải sửa vòng lại hơn.

## 4. Đóng góp khác

- Hỗ trợ nhóm chuyển ý tưởng từ đặc tả thành prototype có thể demo: nhập hành trình, gọi backend, nhận kết quả xếp hạng và hiển thị trạng thái lỗi/không chắc.
- Giữ luồng chính của app đơn giản để các bạn khác có thể gắn thêm component như `SearchForm`, `ResultsList`, `PriorityControl` và `ChatAssistant`.
- Debug các lỗi thường gặp khi tích hợp local như sai endpoint, thiếu CORS, backend chưa chạy hoặc response không khớp type frontend.

## 5. Điều học được

Mình học được rằng phần "base" của sản phẩm AI không chỉ là dựng server và page đầu tiên. Nó quyết định cách các path của AI được biểu diễn xuyên suốt từ backend tới UI. Nếu backend chỉ trả một dạng response cho happy path, frontend rất dễ bị động khi gặp failure hoặc clarification.

Việc làm SmartTravel AI cũng giúp mình thấy rõ vai trò của contract giữa backend và frontend. Khi schema có đủ `path`, `warning`, `decision`, `tickets`, `clarification_options` và `suggested_dates`, UI có thể phản ứng đúng mà không cần đoán logic của agent.

## 6. Nếu làm lại

Mình sẽ chốt API contract sớm hơn bằng một file mock response hoặc OpenAPI example cho từng path: happy, low-confidence, failure và clarification. Như vậy các bạn frontend và backend có thể làm song song mà ít lệch nhau.

Mình cũng sẽ bổ sung test tích hợp đơn giản cho các endpoint chính và một checklist chạy demo: start backend, start frontend, test `/health`, test search input mẫu. Những việc nhỏ này giúp giảm rủi ro ngay trước lúc demo.

## 7. AI giúp gì / AI sai gì

**Giúp:** AI hỗ trợ mình draft nhanh cấu trúc FastAPI route, gợi ý cách tổ chức state trong Next.js page và viết fallback message khi API lỗi. AI cũng hữu ích khi cần chuyển requirement trong SPEC thành checklist kỹ thuật.

**Sai/mislead:** AI đôi khi đề xuất architecture quá lớn cho prototype ngắn ngày, ví dụ tách nhiều layer hoặc thêm state management không cần thiết. Mình phải giữ scope lại: ưu tiên luồng demo chạy ổn, API rõ, lỗi hiện minh bạch và các component đủ dễ để nhóm cùng tích hợp.
