# SmartTravel AI Planner - Hackathon Scope Refinement

## Mục tiêu

Biến sản phẩm từ:

```
User
 ↓
Search
 ↓
Show Results
```

thành:

```
User
 ↓
Planning Agent
 ↓
Search
 ↓
Extract
 ↓
Normalize
 ↓
Compare
 ↓
Rank
 ↓
Decision
 ↓
Generate Itinerary
```

Để chứng minh đây là một AI Agent thực sự thay vì chatbot có search.

---

# 1. Product Positioning

## Không phải

Travel Search Engine

Hiển thị:

* Tavily Result #1
* Tavily Result #2
* Tavily Result #3

=> Không tạo giá trị.

---

## Phải là

SmartTravel AI Planner

User chỉ nhập:

* Destination
* Budget
* Duration
* Travelers

Ví dụ:

```
Tôi muốn đi Đà Nẵng
3 ngày
5 triệu
2 người
```

Agent tự:

* Thu thập dữ liệu
* Phân tích giá
* So sánh phương án
* Đưa ra quyết định
* Sinh itinerary

---

# 2. New Agent Workflow

## Current

```
User
 ↓
Search
 ↓
Show Search Result
```

---

## New

```
User Request
 ↓
Planner Agent
 ↓
Search Agent
 ↓
Data Extraction
 ↓
Normalization
 ↓
Ranking
 ↓
Decision Engine
 ↓
Travel Recommendation
 ↓
Itinerary Generator
```

---

# 3. Structured Data Extraction

Sau khi search web.

KHÔNG đưa raw text cho user.

Agent phải convert thành dữ liệu chuẩn.

Ví dụ:

```json
{
  "transport_type": "bus",
  "provider": "Phuong Trang",
  "price": 420000,
  "departure": "22:00",
  "arrival": "08:00",
  "pickup": "Ben xe My Dinh"
}
```

---

Khách sạn:

```json
{
  "hotel_name": "Hotel A",
  "price_per_night": 700000,
  "rating": 4.2,
  "distance_to_center": 1.5
}
```

---

Nhà hàng:

```json
{
  "restaurant": "Bun Cha Ca",
  "average_cost": 80000,
  "category": "Local Food"
}
```

---

# 4. Data Collection Panel

## Remove

```
Tavily Result #1
Tavily Result #2
Tavily Result #3
```

---

## Add

### Data Collected From Web

#### Transportation

| Type   | Price |
| ------ | ----- |
| Bus    | 420k  |
| Train  | 650k  |
| Flight | 1.2M  |

---

#### Hotels

| Hotel   | Price |
| ------- | ----- |
| Hotel A | 700k  |
| Hotel B | 850k  |
| Hotel C | 950k  |

---

#### Food Estimate

| Category   | Cost/day |
| ---------- | -------- |
| Local Food | 200k     |
| Mixed      | 350k     |
| Premium    | 600k     |

Panel này chứng minh Agent đã thu thập dữ liệu trước khi ra quyết định.

---

# 5. Ranking Engine

Sau khi normalize.

Agent chấm điểm từng lựa chọn.

Ví dụ:

```json
{
  "option": "Bus + Hostel",
  "total_cost": 4600000,
  "comfort_score": 5,
  "speed_score": 4,
  "budget_fit": 10
}
```

---

```json
{
  "option": "Flight + Hotel 3*",
  "total_cost": 5200000,
  "comfort_score": 8,
  "speed_score": 9,
  "budget_fit": 7
}
```

---

Agent sau đó xếp hạng.

```
Score =
0.5 * BudgetFit +
0.3 * Comfort +
0.2 * Speed
```

Không cần ML.

Rule-based là đủ cho demo.

---

# 6. AI Recommendation Section

Đây phải là output chính.

---

## Option 1 - Tiết Kiệm

Tổng chi phí:

4.6 triệu

Bao gồm:

* Xe khách
* Hostel
* Ăn địa phương

Lý do AI chọn:

* Phù hợp ngân sách
* Chi phí thấp nhất
* Đủ cho 3 ngày

---

## Option 2 - Cân Bằng

Tổng chi phí:

5.2 triệu

Bao gồm:

* Máy bay
* Khách sạn 3 sao

Lý do AI chọn:

* Di chuyển nhanh
* Trải nghiệm tốt hơn
* Vượt ngân sách nhẹ

---

## Option 3 - Thoải Mái

Tổng chi phí:

7.5 triệu

Bao gồm:

* Máy bay
* Khách sạn 4 sao

Lý do AI chọn:

* Tiện nghi cao nhất
* Phù hợp nghỉ dưỡng

---

# 7. Itinerary Generation

Sau khi Agent chọn phương án.

Sinh lịch trình.

Ví dụ:

## Day 1

* Đến Đà Nẵng
* Check-in khách sạn
* Cầu Rồng
* Chợ đêm Sơn Trà

---

## Day 2

* Bà Nà Hills
* Ăn đặc sản địa phương

---

## Day 3

* Mỹ Khê
* Mua quà
* Trở về

---

# 8. Low Confidence Panel

Nếu user nhập:

```
Tôi muốn đi Đà Nẵng
```

Không đủ dữ liệu.

Không search ngay.

Hiển thị:

### Tôi cần thêm thông tin

#### Thời gian

* 1-2 ngày
* 3-4 ngày
* 5+ ngày

#### Ngân sách

* < 3 triệu
* 3-6 triệu
* > 6 triệu

#### Số người

* 1
* 2
* 3+

Sau khi user chọn mới chạy Agent.

Điểm cộng lớn khi demo.

---

# 9. Failure Panel

Nếu không tìm được giá.

Hiển thị:

### Không thể xác minh giá hiện tại

Nguyên nhân:

* Nguồn dữ liệu thiếu
* Website không phản hồi
* Giá không còn khả dụng

Bạn muốn:

* Đổi ngày
* Đổi phương tiện
* Tìm khu vực khác

Không để chatbot trả về lỗi kỹ thuật.

---

# 10. Correction / Re-ranking Panel

Sau khi Agent đề xuất.

Hiển thị:

### Ưu tiên hiện tại

✓ Tiết kiệm

---

Cho phép đổi:

* Tiết kiệm
* Nhanh nhất
* Gần trung tâm
* Thoải mái nhất

---

Agent rerank.

KHÔNG search lại.

Chỉ dùng dữ liệu đã thu thập.

Đây là bằng chứng Agent có reasoning.

---

# 11. UI Priority (4 giờ cuối)

## Must Have

* Planner Agent Flow
* Data Collection Panel
* Recommendation Panel
* Itinerary Generator
* Low Confidence Panel
* Re-ranking Panel

---

## Nice To Have

* Streaming Agent Steps
* Memory
* Maps
* Charts

Có thể bỏ.

---

# 12. Demo Story

Người demo nhập:

```
Tôi muốn đi Đà Nẵng
3 ngày
5 triệu
2 người
```

Màn hình:

Step 1:

```
Searching transportation...
```

Step 2:

```
Extracting prices...
```

Step 3:

```
Normalizing data...
```

Step 4:

```
Ranking options...
```

Step 5:

```
Generating itinerary...
```

Sau đó hiện:

* Data Collected From Web
* AI Recommendation
* Travel Plan

=> Giám khảo nhìn thấy rõ Agent đang thực hiện nhiều bước và ra quyết định từ dữ liệu thay vì chỉ gọi search rồi hiển thị kết quả.

# Kết luận

MVP cuối cùng cần chứng minh:

1. Agent tự quyết định cần search gì.
2. Agent trích xuất dữ liệu có cấu trúc.
3. Agent so sánh nhiều lựa chọn.
4. Agent giải thích lý do chọn.
5. Agent sinh itinerary từ quyết định.

Nếu làm được 5 điểm này thì sản phẩm đã đúng tinh thần "AI Agent thực chiến" của hackathon VINUNI.
