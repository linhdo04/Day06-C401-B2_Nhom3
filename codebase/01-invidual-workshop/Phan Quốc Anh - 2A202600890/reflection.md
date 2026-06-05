# Individual reflection — Phan Quốc Anh (2A202600890)

## 1. Role

Backend feature developer, researcher, và ideator - chịu trách nhiệm thiết kế hệ thống schema dữ liệu, xây dựng thuật toán xếp hạng phương án di chuyển theo tiêu chí ưu tiên, tích hợp Agent Service với Gemini API (ReAct flow), và nghiên cứu insight/competitors để hoàn thiện SPEC.

## 2. Đóng góp cụ thể

- **Phát triển thuật toán xếp hạng (`backend/app/agent/ranking.py`)**: Cài đặt logic re-rank linh hoạt dựa trên ưu tiên của người dùng (`Priority.price` - ưu tiên giá thấp, `Priority.time` - ưu tiên giờ đi sớm, `Priority.pickup_distance` - ưu tiên điểm đón gần), tự động sinh lý do xếp hạng (`rank_reason`) cụ thể cho từng vé nhằm tăng tính minh bạch và tạo dựng niềm tin (Trust) với người dùng.
- **Xây dựng lõi xử lý nghiệp vụ (`backend/app/agent/service.py`)**:
  - Hiện thực hóa hàm `search_trip()` đóng vai trò orchestrator điều phối việc trích xuất intent chuyến đi, phát hiện nhập nhằng điểm đón (NER "Thanh Phong"), tìm vé nội bộ và gọi Tavily web search fallback khi thiếu dữ liệu.
  - Thiết kế logic `_build_travel_plan` để tự động tổng hợp phương tiện, khách sạn (`_estimate_hotels`), ăn uống (`_estimate_food`) thành các gói kế hoạch (Budget, Balanced, Comfort) được chấm điểm budget fit và sinh lịch trình (`_generate_itinerary`) chi tiết từng ngày.
- **Tích hợp Gemini Chat Agent với ReAct Loop (`chat_agent()`)**: Sử dụng Gemini API Client bản mới nhất kết hợp với Function Calling để cho phép Agent tự động chọn và thực thi các tools (`search_and_format_tickets`, `search_by_date_tool`, `resolve_pickup_ambiguity_tool`, `search_travel_guide_tool`, `search_stay_options_tool`) nhằm trả lời các câu hỏi tự do của người dùng
- **Nghiên cứu thị trường và đối thủ (`codebase/02-group-spec/evidence-pack.md`)**: Phân tích hành vi người dùng và mô hình của Vexere, MoMo Travel, Google Maps để tìm ra pain point thực tế, giúp nhóm có cơ sở vững chắc chuyển scope sản phẩm từ tìm vé xe thuần túy sang trợ lý quyết định chuyến đi ngắn ngày.

## 3. SPEC mạnh/yếu

- **Mạnh nhất**: SPEC đã xác định đúng đắn hướng đi của SmartTravel AI là **Augmentation** (tăng cường năng lực ra quyết định) thay vì tự động đặt vé hoàn toàn. Nhờ đó, backend ranking và service tập trung tối đa vào tính minh bạch, đưa ra lý do khuyến nghị, cảnh báo tin cậy thấp và đính kèm Maps/booking link để người dùng tự kiểm tra, thay vì phải xử lý các bài toán đặt chỗ/thanh toán đầy rủi ro.
- **Yếu nhất**: Bằng chứng thực tế (user evidence) ngoài nhóm ở phiên bản đầu của SPEC còn tương đối mỏng và dựa nhiều vào giả định. Việc chưa có dữ liệu thời gian thực (real-time) cho các phương tiện tàu/máy bay khiến một số tính toán tổng chi phí trong prototype vẫn dừng lại ở mức ước tính (planning estimate), cần hiển thị warning rõ ràng trên UI để tránh misleading.

## 4. Đóng góp khác

- Góp phần định hình ý tưởng mở rộng scope sản phẩm từ "SmartBus AI" sang "SmartTravel AI" để giải quyết bài toán lớn hơn: chuẩn bị một chuyến đi ngắn ngày thay vì chỉ đi tìm một chiếc vé xe khách.
- Phối hợp chặt chẽ với các thành viên frontend để chuẩn hóa cấu trúc dữ liệu JSON trả về, đảm bảo các component phức tạp như `SearchForm`, `PriorityControl`, `ResultsList`, và các panel cảnh báo lỗi hiển thị chính xác các trạng thái tương ứng.
- Đóng góp vào việc thiết lập các kịch bản demo và kiểm thử các case khó (như nhập nhằng điểm đón Giáo xứ / Nhà xe Thanh Phong, tìm kiếm tuyến không có sẵn dữ liệu mock).

## 5. Điều học được

- Tạo dựng một AI Agent thực tế đòi hỏi thiết kế hệ thống dữ liệu (schemas) chặt chẽ và phân định rõ ràng trách nhiệm của từng tool. LLM chỉ hoạt động tốt và ổn định khi được bao bọc bởi một pipeline backend chuẩn hóa, có khả năng validation và kiểm soát lỗi tốt.
- Hiểu rõ triết lý thiết kế sản phẩm AI Augmentation. Thay vì cố gắng để AI làm hết mọi thứ bao gồm cả các hành động có rủi ro cao (như thanh toán/đặt vé), việc AI đóng vai trò cung cấp thông tin, xếp hạng, cảnh báo và để con người ra quyết định cuối cùng là giải pháp thực tế nhất giúp cân bằng giữa trải nghiệm và độ an toàn.
- Kỹ năng thiết kế logic ranking đa tiêu chí và giải thích lý do xếp hạng (Rank Reason) giúp cải thiện đáng kể trải nghiệm người dùng, giúp họ hiểu được lý do tại sao AI lại gợi ý phương án này mà không phải phương án khác.

## 6. Nếu làm lại

- Tôi sẽ thiết kế thêm cơ chế caching cho các kết quả tìm kiếm web (Tavily search) để tối ưu thời gian phản hồi của agent (giảm bớt độ trễ mạng) và tiết kiệm chi phí gọi API.
- Viết thêm nhiều unit test tự động cho module ranking để kiểm tra các hành vi biên (ví dụ: khi budget của user bằng 0, hoặc khoảng cách điểm đón quá xa).
- Tiến hành khảo sát nhanh và thu thập các review, phản hồi thực tế của người dùng từ các app du lịch lớn sớm hơn nữa để làm bằng chứng (evidence) bảo vệ các pain point trong SPEC thuyết phục hơn.

## 7. AI giúp gì / AI sai gì

- **Giúp**: AI giúp viết các đoạn code boilerplate rất nhanh, đặc biệt là các cấu trúc Pydantic schemas, các biểu thức chính quy (regex) dùng để parse ngày tháng/độ ưu tiên từ chat message, và draft nhanh khung sườn cho hệ thống system instruction của chat agent.
- **Sai/mislead**: AI đôi khi đề xuất các thư viện hoặc kiến trúc quá đồ sộ cho một prototype chạy demo (ví dụ gợi ý sử dụng các framework agent phức tạp như LangChain hay AutoGen cùng hệ thống database SQL đầy đủ). Tôi phải chủ động lược bỏ và tối giản hóa, chọn cách gọi trực tiếp Gemini SDK và mock data để giữ cho codebase gọn gàng, hiệu quả và dễ debug trước giờ demo.
