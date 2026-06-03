# Evidence Pack — SmartBus AI

## 1. Nhóm và track

**Tên nhóm:** SmartBus AI  
**Track:** B · Travel & Hospitality  
**Product/app đã chọn:** Vexere, MoMo Travel, Xanh SM link  
**Build slice:** AI gợi ý top 3 vé xe liên tỉnh theo giá, giờ đi và điểm đón gần.

## 2. Self-use evidence

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| User phải so sánh tuyến/ngày trên nhiều nền tảng. | `02-group-spec/assets/evidence/` | Happy / Correction | SPEC cần gom lựa chọn vào một màn hình so sánh. |
| Điểm đón thường là chi tiết quyết định nhưng khó so nhanh bằng mắt. | `02-group-spec/assets/evidence/` | Low-confidence | SPEC cần hiển thị khoảng cách và Maps link. |

## 3. User / review / social evidence

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Mỗi lần đặt vé mất cả tiếng, vừa lọc giờ vừa so giá vừa xem điểm đón có gần nhà không." | Phỏng vấn nhanh cần bổ sung tên/ngày | Người đi tỉnh định kỳ | Mất thời gian ra quyết định. |
| V-App nhầm "Giáo xứ Thanh Phong" thành "Nhà xe Thanh Phong". | Demo chat log trong SPEC | User cần được đón đúng điểm | Lỗi NER có thể dẫn đến chọn nhầm vé/điểm đón. |

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| Vexere | Tìm và lọc vé theo tuyến/ngày. | Card vé rõ giá/giờ/nhà xe. | Có, dùng mock data. |
| MoMo Travel | Tìm dịch vụ du lịch trong app thanh toán. | Booking/deep-link thay vì tự build payment. | Có, deep-link demo. |
| Google Maps | Xác nhận địa chỉ và khoảng cách điểm đón. | Không rút gọn địa chỉ rủi ro. | Có, build Maps link. |

## 5. Evidence -> Insight

Evidence nổi bật nhất: user không thiếu lựa chọn vé, nhưng thiếu hỗ trợ so sánh theo tiêu chí thật của chuyến đi.

Insight: User không chỉ cần danh sách vé. Họ cần một trợ lý quyết định hẹp, biết xếp hạng theo trade-off giữa giá, giờ đi và điểm đón.

Opportunity: AI có thể augment bằng cách gom dữ liệu mock, phát hiện nhập nhằng địa danh/nhà xe, xếp hạng top 3, và buộc user xác nhận ở case rủi ro.

## 6. Evidence đổi SPEC như thế nào?

- [x] Đổi build slice.
- [x] Đổi Auto/Aug decision.
- [x] Đổi 4 paths.
- [x] Đổi failure mode.
- [x] Đổi owner/test plan.

Trước evidence, nhóm nghĩ đến một assistant đặt vé rộng. Sau evidence, nhóm cắt xuống flow gợi ý top 3 vé và xử lý lỗi NER vì đây là lát cắt demo được trong 1 ngày.
