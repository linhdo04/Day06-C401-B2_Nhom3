# SmartBus AI Test Report

## Manual Acceptance Checklist

- [ ] Search mặc định trả 3 lựa chọn.
- [ ] Mỗi card có giá, giờ đi, khoảng cách điểm đón, Maps link và booking link.
- [ ] Đổi priority re-rank mà không nhập lại tuyến.
- [ ] Tuyến chỉ còn 1 vé hiển thị warning.
- [ ] Tuyến không có vé hiển thị suggested dates.
- [ ] `Giáo xứ Thanh Phong` kích hoạt clarification trước khi xếp hạng.
- [ ] Mobile không bị tràn ngang hoặc đè chữ.

## Automated Tests

Backend:

```bash
npm run test:backend
```

UI:

```bash
npm run test:e2e
```

Full suite:

```bash
npm test
```

## Latest Verification

Run on 2026-06-03:

- `npm run test:backend`: 5 passed.
- `npm --prefix frontend run typecheck`: passed.
- `npm --prefix frontend run build`: passed.
- `npm run test:e2e`: 14 passed across Chromium desktop and mobile projects.

Note: `npm --prefix frontend install` reported 2 npm audit findings from dependencies. They were not force-fixed because `npm audit fix --force` can introduce breaking upgrades during the Day 06 demo window.
