# Individual reflection — Lê Hoài Nam (2A202600657)

## 1. Role

Product/spec owner và backend tools contributor - phụ trách tổng hợp SPEC, rà lại hướng sản phẩm từ SmartBus AI sang SmartTravel AI, và hỗ trợ thiết kế/củng cố các backend tools cho agent.

## 2. Đóng góp cụ thể

- Tổng hợp lại SPEC cuối cho SmartTravel AI theo format sản phẩm: bằng chứng, build slice, AI Product Canvas, 4 paths, failure mode và kế hoạch demo.
- Rà lại hướng sản phẩm để không chỉ dừng ở "tìm vé xe", mà mở rộng đúng với prototype hiện tại: tìm phương án di chuyển, ngân sách chuyến đi, số khách, lưu trú, ăn uống và lịch trình cơ bản.
- Hỗ trợ phần backend tools trong `backend/app/agent/tools.py`, gồm tìm vé từ mock data, fallback web search, phát hiện nhập nhằng điểm đón, tạo Google Maps link và booking deep-link.
- Cùng nhóm chốt quyết định sản phẩm là **augmentation**: AI chỉ hỗ trợ xếp hạng/gợi ý, người dùng vẫn là người quyết định và bấm đặt.
- Chuẩn bị demo flow để giải thích các path chính: happy path, low-confidence, failure và clarification "Thanh Phong".

## 3. SPEC mạnh/yếu

- Mạnh nhất: SPEC đã chuyển được từ ý tưởng rộng thành một lát cắt có thể demo rõ: người dùng nhập chuyến đi, AI gom dữ liệu, xếp hạng phương án, ước tính chi phí và cảnh báo khi không chắc. Phần Trust cũng khá rõ vì sản phẩm không cho AI tự đặt vé/thanh toán, mà bắt người dùng xác nhận qua Maps, nguồn web hoặc booking link.
- Yếu nhất: Evidence ngoài nhóm vẫn chưa đủ mạnh. SPEC hiện có ghi nhận phỏng vấn nhanh và tham chiếu Vexere/MoMo/Google Maps, nhưng cần thêm ảnh chụp review, quote có ngày/tên hoặc link nguồn công khai để bảo vệ pain point tốt hơn. Ngoài ra dữ liệu giá/giờ trong prototype còn là mock/estimate nên chưa thể coi là real-time.

## 4. Đóng góp khác

- Giúp nhóm thống nhất lại tên và framing sản phẩm thành SmartTravel AI.
- Hỗ trợ kết nối nội dung SPEC với code thật trong repo để khi demo có thể chỉ ra phần nào đang chạy ở backend, frontend và test.
- Rà lại phân công cuối file SPEC để mỗi thành viên có artifact cụ thể cần giải thích.
- Hỗ trợ giữ scope demo vừa đủ, tránh biến sản phẩm thành một chatbot du lịch quá rộng.

## 5. Điều học được

Trước đây mình nghĩ phần SPEC chủ yếu là mô tả tính năng. Sau khi làm SmartTravel AI, mình hiểu SPEC tốt phải là một lập luận sản phẩm: vì sao user đau, AI quyết định phần nào, sai thì hậu quả gì, và prototype xử lý đường xấu ra sao.

Phần backend tools cũng giúp mình thấy AI agent không chỉ là gọi LLM. Agent cần các tool nhỏ, rõ trách nhiệm: search dữ liệu, normalize city, detect ambiguity, tạo Maps link, tạo booking link. Nếu tool không rõ input/output hoặc không có fallback, UI rất dễ hiển thị kết quả có vẻ thông minh nhưng không đáng tin.

Mình cũng học được rằng mở rộng scope phải đi cùng giới hạn. SmartTravel AI có thể nói về cả chuyến đi, nhưng lát cắt demo vẫn cần giữ ở quyết định hẹp: chọn phương án di chuyển/kế hoạch phù hợp, không tự động đặt vé.

## 6. Nếu làm lại

Mình sẽ lấy evidence ngoài nhóm sớm hơn, ví dụ chụp review từ app đặt vé, phỏng vấn có ghi ngày/tên hoặc lưu lại ảnh note phỏng vấn. Khi evidence chắc hơn, SPEC sẽ bớt cảm giác dựa vào giả định.

Về backend tools, mình sẽ tách rõ hơn dữ liệu nào là mock, dữ liệu nào là web result, dữ liệu nào là planning estimate. UI cũng nên đánh dấu từng loại dữ liệu để người dùng biết mức độ tin cậy trước khi ra quyết định.

Ngoài ra, mình sẽ viết thêm test cho các case ngân sách vượt mức, transport mode là train/flight, và các input nhập nhằng khác ngoài "Thanh Phong".

## 7. AI giúp gì / AI sai gì

- **Giúp:** AI hỗ trợ mình hệ thống hóa SPEC nhanh hơn, đặc biệt là biến các phần code/backend tools thành lập luận sản phẩm: Value, Trust, Feasibility, learning signal và 4 paths. AI cũng giúp gợi ý cách viết failure mode rõ hơn, không chỉ nói "AI sai" mà chỉ ra sai khi nào, ai chịu thiệt và prototype giảm rủi ro ra sao.
- **Sai/mislead:** AI đôi khi có xu hướng mở rộng sản phẩm quá nhiều, ví dụ muốn làm full travel planner, đặt khách sạn, đặt vé và lịch trình tự động. Nếu đi theo hướng đó thì prototype dễ mất focus và vượt quá khả năng demo. Bài học của mình là phải giữ AI trong scope: hỗ trợ suy nghĩ và viết nhanh, nhưng quyết định sản phẩm cuối vẫn phải dựa vào code thật, evidence thật và thời gian build thật.
