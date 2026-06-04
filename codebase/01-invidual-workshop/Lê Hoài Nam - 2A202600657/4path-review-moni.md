# SPEC ITEM · 4 PATHS

# 4 Paths Review — Moni (MoMo)

> User Stories trong Day05 là 4 paths, không phải một dòng happy path.

---

## Bảng tổng quan

| PATH | CÂU HỎI CẦN TRẢ LỜI | VÍ DỤ QUYẾT ĐỊNH UX |
|---|---|---|
| **Happy** | AI đúng và tự tin, user thấy gì? | Gợi ý hiện rõ, accept một thao tác |
| **Low-confidence** | AI không chắc, có hỏi lại không? | Hiện 2–3 lựa chọn hoặc yêu cầu thêm thông tin |
| **Failure** | AI sai, user recover thế nào? | Undo, sửa trực tiếp, chuyển người thật |
| **Correction** | User sửa, data đi vào đâu? | Correction log, cập nhật rule/test set |

---

## Happy Path

**Câu hỏi:** Khi AI đúng và tự tin, user thấy gì?

**Quan sát trên Moni:**
User chọn thẻ gợi ý có sẵn hoặc hỏi câu đơn giản → AI trả lời nhanh theo template tối ưu, văn phong thân thiện, có emoji nhẹ.

**Ví dụ thực tế:**
- Prompt: *"Số dư ví MoMo của tôi"* → AI trả ngay số dư mà không cần thêm bước nào.
- Prompt: *"Chuyển 10 triệu cho mẹ có tính chi tiêu không?"* → AI giải thích đúng quy tắc phân loại mục "Người thân".

**Quyết định UX (to-be):**
Giữ nguyên template phản hồi nhanh. Thêm 1 nút CTA hành động đơn để accept kết quả ngay tại màn hình chat (ví dụ: `[Xem chi tiết giao dịch]`).

---

## Low-confidence Path

**Câu hỏi:** Khi AI không chắc, hệ thống có hỏi lại, show options hoặc chuyển người không?

**Quan sát trên Moni — Chưa có path này.**

Khi gặp từ khóa mơ hồ hoặc intent không rõ ràng:
- AI map bừa vào một danh mục có sẵn mà không thông báo mức độ tự tin.
- AI không hỏi lại để thu hẹp phạm vi ý định.
- Không có cơ chế hiển thị 2–3 tùy chọn để user làm rõ.

**Ví dụ thực tế:**
- Prompt: *"chi tiêu linh tinh là gì?"* → AI nhận diện như keyword cố định, không nhận ra intent mơ hồ.

**Quyết định UX (to-be):**
Khi confidence score < ngưỡng, thay vì trả lời đại: hiển thị câu hỏi thu hẹp kèm 2–3 Suggestion Chips để user chọn nhanh.

```
Moni: "Bạn đang hỏi về:
  [Chi tiêu chưa phân loại]  [Khoản nhỏ lẻ dưới 50k]  [Giao dịch khác]"
```

**Ghi vào SPEC:** `Low-confidence trigger: confidence < 0.6 → show clarification chips, không trả template mặc định.`

---

## Failure Path 

**Câu hỏi:** Khi AI sai, user biết bằng cách nào và sửa thế nào?

**Quan sát trên Moni — 2 failure điển hình:**

**Failure 1 — Nạp tiền "Tự hỏi tự vả":**

| Turn | Ai nói | Nội dung |
|---|---|---|
| 1 | User | *"nạp hộ tôi 500k từ bank"* |
| 2 | Moni | *"Bạn muốn nạp từ ngân hàng nào?"* ← Slot-filling bắt đầu |
| 3 | User | *"ngân hàng MB"* ← Trả lời đúng theo yêu cầu |
| 4 | Moni | *"Mình chỉ hỗ trợ trong phạm vi MoMo..."* ← Từ chối nhầm |

User bị kẹt tại màn hình chat, không có nút thoát, không có hướng dẫn tiếp theo.

**Failure 2 — Chi tiêu trả về 0đ:**
- AI trả `0 giao dịch / 0đ` khi tài khoản có nhiều giao dịch thực.
- Thay vì báo lỗi kỹ thuật rõ ràng, AI dùng câu xoa dịu phản tác dụng.
- User không có nút nào để trigger đồng bộ lại dữ liệu.

**Quyết định UX (to-be):**
- Khi Guardrail từ chối trong slot-filling: thay refusal bằng `[Tự nạp tiền trên MoMo]` deep-link + câu giải thích ngắn.
- Khi dữ liệu rỗng: thay câu văn mẫu bằng nút `[Đồng bộ lịch sử ví]`.

**Ghi vào SPEC:** `Failure recovery: mọi dead-end phải có ít nhất 1 exit action — deep-link, nút chuyển tiếp, hoặc nút gọi CSKH.`

---

## Correction Path

**Câu hỏi:** Khi user sửa, correction có được lưu/log/học lại không hay biến mất?

**Quan sát trên Moni — Chưa có path này.**

- Không có nút *"Báo AI hiểu sai"* hay *"Sửa phân loại"* trên bất kỳ câu trả lời nào.
- Không có Correction Log — mọi sửa đổi bằng cách gõ lại đều bị xử lý như phiên chat mới độc lập.
- Không có Feedback Loop — AI không học lại từ correction của user.
- Khi hội thoại bị gãy, user không có cách nào báo cáo lỗi ngữ cảnh.

**Quyết định UX (to-be):**
Thêm 2 nút nhỏ dưới mỗi response của Moni:

```
👍  👎  [Sửa phân loại này]
```

Khi user bấm 👎 hoặc `[Sửa]`:
- Lưu `{session_id, turn_id, user_correction}` vào Correction Log.
- Dùng data này để cập nhật test set và retrain intent classifier định kỳ.

**Ghi vào SPEC:** `Correction capture: mỗi response cần có feedback widget. Correction data → log → review hàng tuần → cập nhật rule/test set.`

---

## Tóm tắt: Path nào đang có, path nào thiếu

| PATH | Hiện tại | Cần làm |
|---|---|---|
| Happy | Có, hoạt động tốt với câu đơn giản | Thêm CTA accept 1 thao tác |
| Low-confidence | Chưa có | Xây clarification chips + confidence threshold |
| Failure | Có failure nhưng không có recovery | Thêm exit action cho mọi dead-end |
| Correction | Chưa có | Xây feedback widget + correction log pipeline |

---

*BLOCK 4 · USER STORIES — DAY 05*
