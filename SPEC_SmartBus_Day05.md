# SPEC — SmartBus AI · Nhà xe liên tỉnh phân mảnh
**Track:** B · Travel & Hospitality  
**App nhắm đến:** Vexere, Momo, Xanh SM  
**Ngày:** Day 05

---

## Artifact 1 · Evidence Pack

**User:** Người đi tỉnh định kỳ (về quê, du lịch), 20–40 tuổi, quen đặt vé online.

**Pain thật:** Phải mở 3–4 app (Vexere, Momo, Xanh SM, Facebook) để so sánh vé cùng một chuyến. Mất 15–30 phút mỗi lần vì không có công cụ nào tự động gợi ý theo khung giờ + giá + điểm đón gần vị trí.

**Bằng chứng cần thu thập:**
- [ ] Self-use: 1 người trong nhóm thử đặt vé HN → HCM trên Vexere + Momo cùng lúc, chụp màn hình từng bước
- [ ] Screenshot kết quả so sánh 2 app (giá, điểm đón, giờ xe)
- [ ] 1–2 review 1★ trên CH Play / App Store về trải nghiệm tìm vé
- [ ] Phỏng vấn nhanh 1 người ngoài nhóm hay đi xe tỉnh

**Evidence từ file demo (as-is chat log thực tế trên V-App):**
> User: "tìm một vé rẻ nhất cho tôi đến sài gòn và đón tại giáo xứ thanh phong đi"  
> Bot: Đề xuất Nhà xe Thanh Phong (nhầm địa danh với tên hãng xe — lỗi NER)  
> → User phải giải thích lại 2 lần, bot vẫn không tìm được điểm đón chính xác  
> → Kết quả: bot đẩy user sang Hotline 1900 599 997

**Quote đại diện:**  
*"Mỗi lần đặt vé mất cả tiếng, vừa lọc giờ vừa so giá vừa xem điểm đón có gần nhà không"*

---

## Artifact 2 · Opportunity Statement

Người dùng **không thiếu lựa chọn** — họ thiếu **công cụ tổng hợp và ra quyết định**.

Khi phải tự so sánh thủ công trên nhiều nền tảng, họ thường chọn nhà xe quen thay vì phương án tối ưu về giá và điểm đón. Hệ thống chatbot hiện tại (V-App) còn nhầm địa danh với tên hãng xe (lỗi NER), khiến user phải giải thích lại nhiều lần và cuối cùng bị đẩy sang hotline.

Một AI có thể gom dữ liệu từ nhiều nguồn và ra đề xuất cụ thể theo 3 tiêu chí (giờ + giá + khoảng cách điểm đón) sẽ rút ngắn quyết định từ 20+ phút xuống dưới 2 phút.

---

## Artifact 3 · Build Slice

> **Nguyên tắc: 1 user — 1 task — 1 AI decision — 1 output**

| | Nội dung |
|---|---|
| **1 user** | Người ở Hà Nội muốn về Đà Nẵng cuối tuần này |
| **1 task** | Nhập điểm xuất phát, điểm đến, ngày đi, ưu tiên (giá / giờ / điểm đón gần nhất) |
| **1 AI decision** | AI tổng hợp dữ liệu Vexere → tính điểm tổng hợp theo tiêu chí → chọn top 3 vé |
| **1 output** | Card so sánh 3 vé: giá · giờ · khoảng cách điểm đón từ vị trí user (Google Maps) · link đặt ngay |

**Không build trong slice này:**
- Thanh toán tích hợp (deep-link sang Momo/VNPay là đủ)
- Trung chuyển đến bến xe (để Bonus)
- Nhiều hành trình ghép chặng

---

## Artifact 4 · Augment hay Automate?

**Quyết định: Augment** ✅

| | Lý do |
|---|---|
| AI làm | Gom dữ liệu nhiều nguồn, tính điểm tổng hợp, xác thực địa danh vs tên hãng xe, đề xuất top 3 |
| Human giữ quyền | Chọn vé cuối cùng, xác nhận thanh toán, điều chỉnh tiêu chí ưu tiên |

**Vì sao không Automate:** Tự đặt vé cần tích hợp payment + xác thực danh tính — vượt quá scope 1 ngày build.

---

## Artifact 5 · Four Paths

### ✅ Happy case
Vexere có vé trên route, điểm đón rõ ràng, user nhập đủ thông tin.  
→ AI trả top 3 vé đúng tiêu chí trong < 3 giây, kèm Google Maps link điểm đón.

### ⚠️ Low-confidence case
Chỉ còn 1 vé duy nhất, điểm đón cách user > 5km.  
→ AI vẫn hiển thị vé đó nhưng thêm cảnh báo rõ: *"Chỉ còn 1 lựa chọn — điểm đón cách bạn 6.2km"*

### ❌ Failure case
Không có vé nào trên route cho ngày đã chọn.  
→ AI thông báo rõ, tự động gợi ý ngày lân cận có vé (±1 ngày).

### 🔄 Correction case
User đổi tiêu chí ưu tiên (từ "giá rẻ" sang "điểm đón gần nhất").  
→ AI re-rank ngay lập tức, không cần nhập lại từ đầu.

---

## Artifact 6 · Failure Mode Nguy Hiểm Nhất

**⚠️ AI nhầm địa danh với tên hãng xe (lỗi NER)**  
Ví dụ thực tế: "đón tại Giáo xứ Thanh Phong" → bot hiểu là "đặt vé Nhà xe Thanh Phong"  
→ User đặt nhầm vé, ra bến xe không đúng chỗ.

**Cách prototype xử lý:**
1. Khi nhận input có từ khóa nhập nhằng, AI hỏi xác nhận trước: *"Bạn muốn đặt vé Nhà xe Thanh Phong, hay muốn được đón tại địa danh Giáo xứ Thanh Phong ở Phú Mỹ, Vũng Tàu?"*
2. Hiển thị địa chỉ điểm đón đầy đủ (không rút gọn), kèm Google Maps link để user xác nhận trước khi đặt
3. Không tự đặt vé — user phải bấm confirm sau khi đã xem thông tin đầy đủ

---

## Artifact 7 · Owner Plan

| Vai trò | Người phụ trách | Việc cụ thể | File ownership để tránh conflict |
|---|---|---|---|
| **Repo/SPEC** | Member 1 | Cấu hình repo, README, SPEC, script chạy test | `README.md`, `SPEC_SmartBus_Day05.md`, `package.json`, `playwright.config.ts`, `requirements.txt` |
| **Research** | Member 2 | Self-use Vexere + Momo, chụp screenshot, tìm 1–2 review thật | `02-group-spec/evidence-pack.md`, `02-group-spec/thin-spec.md`, `02-group-spec/assets/evidence/*` |
| **Frontend search** | Member 3 | Search form, priority control, gọi API backend | `frontend/app/*`, `frontend/components/SearchForm.tsx`, `frontend/components/PriorityControl.tsx`, `frontend/lib/*` |
| **Python backend** | Member 4 | FastAPI, schemas, agent tools, mock ticket data, backend tests | `backend/app/*`, `backend/tests/test_agent.py` |
| **Result UI** | Member 5 | Ticket cards, warning, failure, clarification panels | `frontend/components/ResultsList.tsx`, `TicketCard.tsx`, `PathStatus.tsx`, `ClarificationPanel.tsx`, `FailurePanel.tsx` |
| **Test/Demo** | Member 6 | Playwright UI test, demo script, test report | `tests/e2e/*`, `docs/demo-script.md`, `docs/test-report.md` |

**Stack Day 06:** Python FastAPI backend + Next.js frontend. Backend dùng mock data, không scrape dữ liệu thật và không tự thanh toán.

---

## Bonus — Sau khi có MVP

### Bonus 1 · Trung chuyển đến bến xe
Tích hợp Xanh SM / Grab → gợi ý xe máy công nghệ từ vị trí user đến bến xe xuất phát.  
Chỉ build sau khi flow chính chạy được.

### Bonus 2 · Thanh toán
Deep-link sang Momo / VNPay thay vì tự build payment — giữ scope nhỏ, demo được ngay.

---

## Flow tối Day 05

```
16:00  Chốt track: Nhà xe liên tỉnh — phân mảnh vé ✅
16:15  Self-use: thử đặt vé thật trên Vexere + Momo, chụp màn hình
16:45  Gom evidence: screenshot + 1 quote từ review / phỏng vấn ngoài nhóm
17:00  Chốt build slice + phân owner cho từng người
Tối    Hoàn thiện SPEC (file này) + bắt đầu prototype nếu còn thời gian
```

---

*Lưu ý: Điền tên thành viên vào cột "Người phụ trách" ở Artifact 7 trước 17:00 hôm nay.*
