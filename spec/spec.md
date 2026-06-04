# SPEC sản phẩm — SmartTravel AI

## 1. Bằng chứng

SmartTravel AI nằm trong track **Travel & Hospitality**. Nhóm ban đầu đi theo hướng SmartBus AI, nhưng sau khi thảo luận lại và đối chiếu với prototype hiện tại, sản phẩm được mở rộng thành trợ lý ra quyết định cho chuyến đi ngắn ngày: tìm phương án di chuyển, ước tính ngân sách và gợi ý lịch trình cơ bản.

### Bằng chứng từ trải nghiệm trực tiếp

| Quan sát | Nguồn trong repo | Nhận định sản phẩm |
|---|---|---|
| Khi chuẩn bị đi tỉnh hoặc du lịch cuối tuần, người dùng phải tự so sánh nhiều yếu tố: giá vé, giờ đi, điểm đón, loại phương tiện, số ngày, số khách và ngân sách. | `02-group-spec/evidence-pack.md`, `frontend/components/SearchForm.tsx` | Pain không chỉ là "tìm vé", mà là ra quyết định giữa nhiều trade-off. |
| Giá rẻ nhất chưa chắc là phương án tốt nhất nếu điểm đón xa, giờ đi bất tiện hoặc vượt ngân sách chuyến đi. | `02-group-spec/thin-spec.md`, `backend/app/agent/ranking.py`, `backend/app/agent/service.py` | AI cần xếp hạng và giải thích, không chỉ lọc danh sách. |
| Chuỗi "Thanh Phong" có thể bị hiểu nhầm giữa địa danh điểm đón và tên nhà xe. | `02-group-spec/thin-spec.md`, `backend/tests/test_agent.py` | Sản phẩm cần hỏi lại khi input nhập nhằng trước khi đưa ra khuyến nghị. |
| Prototype hiện đã có các path happy, low-confidence, failure và clarification. | `backend/app/agent/service.py`, `frontend/components/ResultsList.tsx` | SPEC phải mô tả đầy đủ cách sản phẩm phục hồi khi AI không chắc hoặc thiếu dữ liệu. |

### Bằng chứng ngoài nhóm

| Bằng chứng | Nguồn | Ý nghĩa |
|---|---|---|
| Người dùng được phỏng vấn nhanh nói: "Mỗi lần đặt vé mất cả tiếng, vừa lọc giờ vừa so giá vừa xem điểm đón có gần nhà không." | Ghi trong `02-group-spec/evidence-pack.md`; nhóm cần bổ sung tên/ngày hoặc ảnh chụp ghi chú phỏng vấn trước khi nộp cuối. | Người dùng không thiếu app đặt vé, họ thiếu một lớp hỗ trợ quyết định đáng tin. |
| Các sản phẩm như Vexere, MoMo Travel, Google Maps tách rời từng phần của workflow: tìm vé, đặt dịch vụ, kiểm tra vị trí. | `02-group-spec/evidence-pack.md` | Cơ hội của SmartTravel AI là gom dữ liệu cần so sánh vào một màn hình quyết định, rồi deep-link sang nơi đặt thật. |

Những bằng chứng đã có đủ để bảo vệ lát cắt prototype, nhưng nhóm vẫn cần bổ sung ít nhất một ảnh chụp review, phỏng vấn hoặc bình luận công khai để làm mạnh phần evidence ngoài nhóm.

## 2. Lát cắt để build

Cho **người ở Hà Nội muốn đi Đà Nẵng trong 3 ngày với ngân sách cố định**, prototype dùng AI để **augment quyết định chọn phương án di chuyển và kế hoạch chuyến đi**, tạo ra **danh sách phương tiện được xếp hạng, ước tính khách sạn/ăn uống, phương án tổng chi phí, khuyến nghị cuối và lịch trình ngắn**, đồng thời xử lý lỗi nhập nhằng như **"Thanh Phong"** bằng bước hỏi lại trước khi gợi ý.

Lát cắt này không build toàn bộ app du lịch. Prototype chỉ chứng minh một quyết định hẹp: **nên chọn phương án di chuyển và gói kế hoạch nào cho chuyến đi cụ thể này**.

## 3. AI Product Canvas

| Ô | Nội dung SPEC |
|---|---|
| **Value — Giá trị** | SmartTravel AI dành cho người chuẩn bị chuyến đi ngắn ngày, quen tự đặt dịch vụ online nhưng mất thời gian so sánh nhiều nguồn. AI giúp gom dữ liệu, chuẩn hóa lựa chọn, xếp hạng theo ưu tiên và giải thích vì sao một phương án phù hợp với ngân sách, số khách và lịch đi. |
| **Trust — Niềm tin** | Khi dữ liệu thiếu hoặc AI không chắc, UI chuyển sang low-confidence/failure/clarification thay vì giả vờ chắc chắn. Người dùng thấy warning, nguồn web nếu có, Google Maps link, suggested dates và câu hỏi làm rõ. Người dùng vẫn là người bấm đặt qua booking/deep-link. |
| **Feasibility — Tính khả thi** | Prototype dùng FastAPI backend, Next.js frontend, mock ticket data và fallback Tavily nếu có API key. Chi phí demo thấp vì ranking chạy nội bộ; web search chỉ gọi khi mock không có dữ liệu. Rủi ro lớn nhất là dữ liệu giá/giờ không real-time. Ngưỡng dừng: nếu không có dữ liệu đáng tin hoặc không hiện được nguồn/booking link, hệ thống không được đưa ra khuyến nghị chắc chắn. |
| **Tín hiệu học** | Khi người dùng đổi priority, chọn ngày gợi ý hoặc trả lời clarification, đó là tín hiệu về tiêu chí ra quyết định và lỗi hiểu sai intent. Các case này nên được lưu thành test case/prompt log để cập nhật rule ranking, normalization và bộ kiểm thử regression. |

## 4. Tăng năng lực hay tự động hóa

SmartTravel AI chọn hướng **tăng năng lực người dùng (augmentation)**.

AI được phép:

- Đọc intent chuyến đi: điểm đi, điểm đến, ngày, số ngày, số khách, ngân sách, phương tiện và ưu tiên.
- Tìm dữ liệu vé trong mock data hoặc nguồn web fallback.
- Xếp hạng lựa chọn theo giá, giờ đi hoặc khoảng cách điểm đón.
- Ước tính chi phí lưu trú, ăn uống và tạo lịch trình ngắn.
- Hỏi lại khi input nhập nhằng hoặc dữ liệu không đủ chắc.

AI không được:

- Tự đặt vé, tự thanh toán hoặc tự cam kết giá/giờ là còn hiệu lực.
- Tự bỏ qua cảnh báo khi điểm đón xa, thiếu vé hoặc nguồn dữ liệu không chắc.

Con người giữ quyền quyết định ở bước chọn phương án cuối và mở booking link. Lý do là sai sót trong đặt vé du lịch có thể gây mất tiền, lỡ chuyến hoặc đến sai điểm đón; các hậu quả này không nên để AI tự động hóa trong prototype.

## 5. Bốn đường đi của trải nghiệm

| Đường đi | Prototype thể hiện gì? | Cách xử lý trong code |
|---|---|---|
| **Đường thuận** | Người dùng nhập Hà Nội → Đà Nẵng, ngày `2026-06-06`, 3 ngày, 2 khách. AI trả về phương tiện phù hợp, card vé, chi phí dự kiến và khuyến nghị. | `search_trip()` trả `PathType.happy` hoặc kết quả ranked; `ResultsList` hiển thị ticket cards và planning output. |
| **Khi AI không chắc** | Chỉ còn ít lựa chọn, điểm đón xa hoặc phải dùng dữ liệu web/ước tính. UI hiện warning thay vì kết luận chắc chắn. | `_build_low_confidence_warning()`, `PathType.low_confidence`, `WebResultsPanel`, `PathStatus`. |
| **Khi AI sai hoặc thiếu dữ liệu** | Không có vé/ngày phù hợp hoặc nguồn web không trả kết quả. UI không dựng kết quả giả, mà gợi ý ngày gần nhất nếu có. | `PathType.failure`, `suggest_nearby_dates()`, `FailurePanel`. |
| **Khi người dùng sửa** | Người dùng đổi priority từ giá thấp sang điểm đón gần hoặc đổi ngày gợi ý. Kết quả được re-rank/re-search mà không phải nhập lại toàn bộ form. | `handlePriorityChange()`, `handleSuggestedDate()`, `rank_tickets()`. |

## 6. Những kiểu lỗi đáng lo nhất

### 1. Nhầm địa danh với nhà xe

Lỗi xuất hiện khi người dùng nhập cụm mơ hồ như "Thanh Phong". Nếu AI hiểu nhầm địa danh điểm đón thành nhà xe, người dùng có thể chọn sai điểm đón hoặc bỏ lỡ phương án đúng.

Prototype xử lý bằng `clarification` path: hỏi người dùng muốn nói đến **Giáo xứ Thanh Phong** hay **Nhà xe Thanh Phong**. Sau khi người dùng chọn, hệ thống vẫn hiện cảnh báo kiểm tra địa chỉ đầy đủ và Maps trước khi đặt.

### 2. Dữ liệu giá/giờ không còn đúng

Lỗi xuất hiện khi dữ liệu mock hoặc kết quả web không phản ánh trạng thái bán vé thật. Người chịu thiệt là người dùng vì có thể ra quyết định dựa trên giá/giờ cũ.

Prototype xử lý bằng cách hiển thị booking/deep-link và nguồn web, không tự đặt vé. Các giá trị từ web hoặc planning estimate phải được hiểu là dữ liệu tham khảo cần xác nhận.

### 3. Khuyến nghị vượt ngân sách thực tế

Lỗi xuất hiện khi chi phí phát sinh như di chuyển nội đô, phụ phí hành lý, cuối tuần/cao điểm hoặc thay đổi giá phòng chưa được tính đủ. Người dùng có thể chọn plan tưởng là vừa ngân sách nhưng thực tế vượt chi.

Prototype xử lý bằng `budget_fit`, tổng chi phí dự kiến và decision reason. Nếu tổng chi phí vượt ngân sách, UI cần trình bày như cảnh báo/điểm fit thấp, không nói đây là lựa chọn tối ưu tuyệt đối.

## 7. Kế hoạch kiểm thử và bằng chứng demo

### Input demo đường thuận

```text
Điểm đi: Ha Noi
Điểm đến: Da Nang
Ngày: 2026-06-06
Số ngày: 3
Số khách: 2
Ngân sách: 5,000,000 VNĐ
Phương tiện: Xe hoặc Tất cả
Ưu tiên: Giá thấp
```

Kết quả cần thấy:

- Danh sách phương tiện/ticket options được xếp hạng.
- Lý do xếp hạng theo giá, giờ hoặc điểm đón.
- Tổng chi phí dự kiến cho chuyến đi.
- Khuyến nghị cuối và lịch trình ngắn.
- Booking link và Maps link để người dùng tự xác nhận.

### Input demo khó

```text
Điểm đón/ghi chú: Giao xu Thanh Phong
```

Kết quả cần thấy:

- Agent không vội đưa kết quả.
- UI hỏi lại "Thanh Phong" là địa danh điểm đón hay nhà xe.
- Sau khi chọn địa danh, hệ thống tiếp tục gợi ý nhưng giữ warning kiểm tra Maps.

### Input demo failure/low-confidence

```text
Điểm đi: Ha Noi
Điểm đến: Nha Trang
Ngày: 2026-06-06
```

Kết quả cần thấy:

- Nếu không có vé nội bộ và không có Tavily result, hệ thống trả failure.
- UI gợi ý ngày gần nhất có dữ liệu, ví dụ `2026-06-07`.
- Hệ thống không bịa vé để lấp màn hình.

### Bằng chứng cần giữ lại

- Ảnh chụp màn hình các path: happy, correction, failure, clarification.
- Nhật ký test backend trong `backend/tests/test_agent.py`.
- Demo script trong `docs/demo-script.md`, cần cập nhật tên SmartTravel AI.
- Evidence pack trong `02-group-spec/evidence-pack.md`, cần cập nhật từ SmartBus AI sang SmartTravel AI.
- Prompt hoặc log mô tả cách nhóm quyết định chuyển từ vé xe hẹp sang planning di chuyển/chuyến đi.

## 8. Phân công

| Thành viên | Phụ trách | Artifact cần giải thích khi demo |
|---|---|---|
| Lê Hoài Nam | Tổng hợp SPEC, rà lại hướng SmartTravel AI, backend tools | `spec/spec.md`, `backend/app/agent/tools.py`, demo flow |
| Đỗ Thiện Lĩnh | Giữ repo, git control, task tracking, build docker điều phối vai trò  | README, cấu trúc repo, git history/task tracking |
| Đào Xuân Bách | Backend and frontend base, bug fix, transpose idea  | `backend/app/main.py`, `frontend/app/page.tsx`, luồng kết nối frontend-backend |
| Nguyễn Đức Kiên Trung | Frontend form tìm kiếm và control ưu tiên, chat assistant  | `frontend/components/SearchForm.tsx`, `frontend/components/PriorityControl.tsx`, `frontend/components/ChatAssistant.tsx`, `frontend/app/api/chat/route.ts` |
| Phan Quốc Anh | Backend feature, research, idea  | `backend/app/schemas.py`, `backend/app/agent/service.py`, `backend/app/agent/ranking.py`, `02-group-spec/evidence-pack.md` |
| Nhân Khánh Đình  | Kiểm thử, demo script, QA, UI kết quả  | `backend/tests/test_agent.py`, `docs/demo-script.md`, `docs/test-report.md`, `frontend/components/ResultsList.tsx`, `frontend/components/ClarificationPanel.tsx`, `frontend/components/FailurePanel.tsx` |
