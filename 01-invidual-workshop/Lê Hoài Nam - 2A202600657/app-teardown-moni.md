# Workshop — Mổ App AI Thật: Moni (MoMo)

**Thời gian thực hiện:** Lab Day 05  
**Sản phẩm:** Moni — Trợ lý tài chính AI tích hợp trong siêu ứng dụng MoMo  
**Output:** Finding notes theo 5 luồng + 4 paths + product decisions + spec mapping \
**Học Sinh:** Lê Hoài Nam - 2A202600657

---

## 1. Chọn sản phẩm để dùng thử

| Sản phẩm | AI feature | Cách truy cập |
|---|---|---|
| MoMo — Moni | Trợ lý tài chính, phân tích chi tiêu, chatbot | App MoMo |

---

## 2. Dùng thử: promise vs reality

### Luồng 1 — Xem chi tiêu lịch sử

- **Product hứa gì:** Moni là trợ lý tài chính thông minh, liên kết trực tiếp với dữ liệu giao dịch ví MoMo, tự động phân nhóm danh mục và đưa ra insight cụ thể (ví dụ: *"Bạn chi 42% cho ăn uống, tăng 18% so với tháng trước"*).
- **User nào được hứa sẽ được giúp:** Người dùng muốn kiểm soát và hiểu rõ thói quen chi tiêu cá nhân.
- **Kỳ vọng AI làm được task nào:** Truy xuất và tóm tắt chi tiêu tháng theo danh mục.
- **Điểm gãy xuất hiện ở đâu:** AI trả về `0đ` với `0 giao dịch`, dù tài khoản thực tế có phát sinh nhiều giao dịch. Thay vì báo lỗi rõ ràng, AI dùng câu xoa dịu: *"Có vẻ bạn đang sống như một thiền sư, hoặc chưa ghi chép chi tiêu vào MoMo..."* — phản tác dụng và mất lòng tin người dùng.

**Evidence:** Câu phản hồi trực tiếp từ app khi hỏi *"Tháng này tôi tiêu nhiều nhất vào khoản nào?"*

---

### Luồng 2 — Ý định giả định tương lai

- **Product hứa gì:** AI hiểu ngữ cảnh câu hỏi dạng giả định, hỗ trợ tư vấn quy tắc tài chính linh hoạt.
- **User nào được hứa sẽ được giúp:** Người dùng muốn hiểu rõ quy tắc phân loại chi tiêu trước khi thực hiện giao dịch.
- **Kỳ vọng AI làm được task nào:** Giải thích xem khoản chuyển tiền cho mẹ có tính là chi tiêu không.
- **Điểm gãy xuất hiện ở đâu:** AI hiểu đúng quy tắc nhưng bị lỗi **Intent Rush** — dù câu hỏi chỉ là giả định ở tương lai, AI ngay lập tức đòi kích hoạt tác vụ ghi chép thực: *"Bạn muốn Moni giúp ghi chép khoản chuyển tiền này vào mục 'Người thân' không?"* Hơn nữa, câu hỏi xác nhận không kèm Suggestion Chips (nút Có/Không), ép user phải tự gõ tay.

**Evidence:** Prompt thử: *"Tôi sẽ nạp vào và chuyển 10 triệu cho mẹ thì có tính là chi tiêu không"* — quan sát hành vi AI đặt câu hỏi đóng không có nút tương tác.

---

### Luồng 3 — Nạp tiền từ ngân hàng (lỗi "Tự hỏi tự vả")

- **Product hứa gì:** AI hỗ trợ thực thi tác vụ nhanh qua hội thoại, bao gồm dẫn dắt luồng nạp tiền.
- **User nào được hứa sẽ được giúp:** Người dùng muốn nạp tiền ví nhanh qua chat thay vì tự tìm tính năng.
- **Kỳ vọng AI làm được task nào:** Slot-filling tên ngân hàng, sau đó chuyển sang màn hình xác nhận giao dịch.
- **Điểm gãy xuất hiện ở đâu:** AI khởi động slot-filling tốt (hỏi tên ngân hàng), nhưng khi nhận được câu trả lời *"ngân hàng MB"*, AI mất context và kích hoạt sai Guardrail, trả ra: *"Mình là Moni, trợ lý của MoMo. Mình chỉ có thể hỗ trợ trong phạm vi sản phẩm MoMo."* — cắt đứt hoàn toàn luồng giao dịch do chính mình dẫn dắt.

**Evidence:** Đoạn hội thoại 4 turns thực tế — Turn 2 AI yêu cầu tên ngân hàng, Turn 4 AI từ chối sau khi user cung cấp đúng thông tin.

---

### Luồng 4 — Lặp hội thoại vô tận

- **Product hứa gì:** AI nhận ra cùng một mối lo ngại dù diễn đạt khác nhau, chuyển sang giải pháp sâu hơn thay vì lặp lại.
- **User nào được hứa sẽ được giúp:** Người dùng lo lắng về tình trạng chi tiêu, muốn được tư vấn hành động cụ thể.
- **Kỳ vọng AI làm được task nào:** Nhận ra intent trùng lặp và đề xuất công cụ lập ngân sách.
- **Điểm gãy xuất hiện ở đâu:** AI coi mỗi câu là một lệnh mới độc lập, liên tục lặp lại template *"Bạn có muốn xem mẹo tiết kiệm không?"*, tạo vòng lặp không lối thoát.

**Evidence:** Prompt lặp: *"tháng này tôi tiêu quá tay rồi đúng không"* → *"tôi tiêu hơi quá tay tháng này"* — AI trả ra cùng một response rập khuôn.

---

### Luồng 5 — Tư vấn lập kế hoạch tài chính

- **Product hứa gì:** AI đưa ra hướng dẫn ngắn gọn, trực quan, kết nối hành động với các tính năng MoMo sẵn có.
- **User nào được hứa sẽ được giúp:** Người dùng muốn lập kế hoạch tài chính hoặc tìm giải pháp mua sắm lớn.
- **Kỳ vọng AI làm được task nào:** Tư vấn ngắn + dẫn link/nút tới tính năng liên quan trong app.
- **Điểm gãy xuất hiện ở đâu:** AI trả ra "bức tường chữ" dài, không có nút Deep-link nào dẫn vào tính năng Quản lý chi tiêu hay Dịch vụ vay tài chính của MoMo — biến AI thành chatbot thông tin thuần túy, không chuyển đổi được người dùng sang dịch vụ.

**Evidence:** Prompt thử: *"Tôi muốn tự lập bảng chi tiêu cá nhân"*, *"Mua oto gì rẻ cho tôi"* — quan sát output chỉ toàn text, không có CTA nào.

---

## 3. Vẽ 4 paths

| Path | Quan sát trên Moni |
|---|---|
| **Happy** | User hỏi câu đơn giản hoặc chọn thẻ gợi ý có sẵn → AI trả lời nhanh theo template đã tối ưu. |
| **Low-confidence** | Chưa có. Khi gặp từ khóa mơ hồ (ví dụ: "linh tinh"), AI map bừa vào một danh mục hoặc trả văn mẫu chung chung, không hỏi lại hay đưa 2–3 tùy chọn để user làm rõ. |
| **Failure** | Luồng nạp tiền: AI dẫn dắt slot-filling rồi tự từ chối khi nhận được câu trả lời đúng. Luồng chi tiêu: Trả `0đ`, đổ lỗi user chưa nhập tay — gây mất tin tưởng nghiêm trọng. |
| **Correction** | Chưa có. Không có nút "Báo AI hiểu sai", không có Correction Log, không có Feedback Loop. Mọi sửa đổi của user đều bị xử lý như phiên chat mới, không kế thừa để cải thiện hệ thống. |

---

## 4. Viết finding thành quyết định

### Finding 1 — Lỗi từ chối nhầm trong luồng Slot-filling

```
Khi user cung cấp tên ngân hàng đối tác ("ngân hàng MB") để hoàn thành
câu hỏi thu thập dữ liệu do chính AI đặt ra trong luồng nạp tiền,
AI bị mất context và kích hoạt sai Guardrail từ chối,
hậu quả là đứt gãy hoàn toàn luồng giao dịch cốt lõi, sụt giảm
Transaction Conversion Rate qua kênh trợ lý ảo.
Lỗi thuộc layer Safety/Behavior + Intent.
Nên sửa bằng Dialogue State Machine: khi Current_State == SLOT_FILLING_BANK,
bypass bộ lọc Out-of-scope Guardrail cho toàn bộ danh sách ngân hàng
trong Linked_Bank_Entities_List. Đo bằng False Positive Refusal Rate < 0.2%.
```

### Finding 2 — Trả dữ liệu rỗng và vòng lặp hội thoại

```
Khi user hỏi về chi tiêu tháng hoặc lặp lại cùng một nỗi lo lắng tài chính,
AI trả về 0đ (do thiếu sync dữ liệu thời gian thực) và liên tục lặp
lại template câu hỏi rập khuôn,
hậu quả là người dùng mất tin vào năng lực AI, cuộc hội thoại đi vào
ngõ cụt, user drop-off cao.
Lỗi thuộc layer Promise + Data/Tool + UX Recovery.
Nên sửa bằng: (1) API tự động sync dữ liệu giao dịch khi nhận Intent
"Hỏi chi tiêu", thay empty state bằng nút [Đồng bộ lịch sử ví MoMo];
(2) Repetition Penalty — nếu Similarity(Turn_N, Turn_N-1) > 0.85,
cấm dùng lại template cũ, đẩy thẳng widget thiết lập ngân sách.
Đo bằng User Drop-off Rate tại phiên quản lý chi tiêu < 10%.
```

### Finding 3 — Tư vấn cô lập, không kết nối hành động

```
Khi user yêu cầu lập kế hoạch tài chính hoặc hỏi về mua sắm lớn,
AI trả ra "bức tường chữ" thuần text, hoàn toàn cô lập với hệ sinh thái
dịch vụ MoMo,
hậu quả là tỷ lệ thoát luồng chat cao, không chuyển đổi được user
chatbot thành user tính năng dịch vụ.
Lỗi thuộc layer UX Presentation + Data/Tool.
Nên sửa bằng Progressive Disclosure (text tóm tắt ≤ 3 dòng, chi tiết
trong Carousel) + bắt buộc đính kèm nút CTA Deep-link dẫn thẳng vào
tính năng tương ứng trong app (ví dụ: [Mở Trình Quản Lý Chi Tiêu MoMo]).
Đo bằng CTR vào Deep-link nội bộ ≥ 15%.
```

---

## 5. Sketch as-is / to-be

### As-is (Luồng nạp tiền — điểm gãy tiêu biểu)

```
User: "nạp hộ tôi 500k từ bank"
        ↓
AI: "Từ ngân hàng nào?" ← [Slot-filling bắt đầu tốt]
        ↓
User: "ngân hàng MB"
        ↓
AI: "Mình chỉ hỗ trợ trong phạm vi MoMo..." ← ĐIỂM GÃY
        (Context bị reset, Guardrail kích hoạt sai)
        ↓
User bị kẹt tại màn hình chat, không có lối thoát
```

### To-be (Luồng đã sửa)

```
User: "nạp hộ tôi 500k từ bank"
        ↓
AI: "Từ ngân hàng nào?" ← State: SLOT_FILLING_BANK
        ↓
User: "ngân hàng MB"
        ↓
[State Lock: bypass Guardrail, parse vào Bank_Slot] ← ĐÃ SỬA
        ↓
AI hiển thị: màn hình xác nhận giao dịch nạp 500k từ MB
        ↓
User xác nhận → Giao dịch hoàn thành
```

---

## 6. Tự kiểm trước khi nộp

- [x] Có ít nhất 1 screenshot hoặc observation cụ thể (quotes trực tiếp từ app, đoạn hội thoại 4 turns luồng nạp tiền).
- [x] Có đủ 4 paths — Low-confidence và Correction được ghi rõ là **chưa tồn tại** trong product hiện tại.
- [x] Finding được viết thành product decision theo công thức: trigger → failure → impact → layer → fix → metric.
- [x] Sketch có as-is (đánh dấu điểm gãy) và to-be (đánh dấu path đã sửa).
- [x] Mỗi finding nói rõ sẽ đổi gì trong SPEC: Dialogue State Control, Repetition Penalty, Progressive Disclosure + Deep-link CTA.
