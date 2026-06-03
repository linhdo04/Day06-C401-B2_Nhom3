# Thin SPEC — SmartBus AI

## 1. Track, product/app và user

**Track:** Travel & Hospitality  
**Product/app thật:** Vexere, MoMo Travel, Xanh SM link  
**User cụ thể:** Người ở Hà Nội muốn đi Đà Nẵng cuối tuần, quen đặt vé online.  
**Nhóm có phải user thật không?** Có một phần: nhóm có thể tự trải nghiệm workflow tìm vé, nhưng cần bổ sung quote ngoài nhóm.

## 2. Evidence summary

| Evidence | Nguồn | User/pain nói lên điều gì? | SPEC phải đổi gì? |
|---|---|---|---|
| So sánh vé trên nhiều app tốn 15-30 phút. | Self-use / phỏng vấn nhanh | User cần decision support, không chỉ filter. | Build màn hình xếp hạng top 3. |
| Điểm đón gần nhà là tiêu chí quan trọng. | Self-use | Giá rẻ nhất chưa chắc tốt nhất. | Thêm priority `pickup_distance`. |
| "Thanh Phong" có thể là địa danh hoặc nhà xe. | Demo chat log | Lỗi NER nguy hiểm. | Thêm clarification path. |

## 3. Pain statement

```text
User đi tỉnh đang gặp khó ở bước chọn vé,
vì phải tự so sánh giá, giờ đi và điểm đón trên nhiều nền tảng,
dẫn tới mất thời gian và có thể chọn phương án không tối ưu.
Bằng chứng chính là self-use, quote phỏng vấn và lỗi NER Thanh Phong.
```

## 4. Build slice

```text
Cho người ở Hà Nội muốn đi Đà Nẵng cuối tuần,
prototype sẽ dùng AI để augment việc xếp hạng vé xe liên tỉnh,
tạo ra top 3 card vé có giá, giờ đi, khoảng cách điểm đón, Maps link và booking link,
và xử lý lỗi nhầm địa danh/nhà xe bằng clarification trước khi gợi ý.
```

## 5. Auto/Aug decision

- [x] **Augmentation:** AI gợi ý/draft/phân loại, user quyết cuối.
- [ ] **Conditional automation:** AI tự làm trong case hẹp; case mơ hồ/rủi ro chuyển người.
- [ ] **Automation:** AI tự quyết và tự hành động.

**Lý do chọn:** Tự đặt vé/thanh toán vượt scope và rủi ro cao.  
**Human role:** decider.

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| Happy | Hà Nội -> Đà Nẵng có 3 vé, agent xếp hạng và show Maps/booking link. |
| Low-confidence | Chỉ còn 1 vé hoặc điểm đón xa, UI hiển thị warning rõ. |
| Failure | Không có vé ngày đã chọn, UI gợi ý ngày gần nhất có dữ liệu. |
| Correction | User đổi priority, kết quả re-rank không cần nhập lại tuyến. |

## 7. Failure mode nguy hiểm nhất

```text
Nếu user nhập "Giáo xứ Thanh Phong",
AI có thể hiểu nhầm là "Nhà xe Thanh Phong",
hậu quả là user chọn nhầm điểm đón/nhà xe.
Prototype sẽ xử lý bằng clarification panel và Maps link trước khi user đặt vé.
Owner kiểm thử path này là Member 6.
```

## 8. Owner plan cho sáng Day 06

| Thành viên | Việc phụ trách | Bằng chứng cần có trong repo |
|---|---|---|
| Member 1 | Repo/config/spec | README, SPEC, package/config files |
| Member 2 | Research/evidence | Evidence pack, screenshots folder |
| Member 3 | Frontend search UI | Search form, priority control |
| Member 4 | Python backend agent | FastAPI schemas, tools, mock data, backend tests |
| Member 5 | Result/failure UI | Ticket cards, clarification/failure panels |
| Member 6 | Test/demo/repo QA | Playwright tests, demo script, test report |
