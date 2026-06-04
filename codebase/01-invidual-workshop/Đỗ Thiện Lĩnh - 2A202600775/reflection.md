# Individual reflection — 2A202600775_Đỗ Thiện Lĩnh

## 1. Role
Giữ repo, kiểm soát git, theo dõi task, build Docker và điều phối môi trường (repo maintainer / release coordinator).

## 2. Đóng góp cụ thể
- Thiết lập và duy trì quy ước git: branching strategy, hướng dẫn tạo PR, review checklist.
- Quản lý task và tiến độ: tạo/assign issue, milestone, cập nhật trạng thái task cho nhóm.
- Hỗ trợ build Docker và điều phối: chuẩn hóa `Dockerfile`/`docker-compose.yml`, build image cho demo, hướng dẫn chạy môi trường local.
- Hỗ trợ đồng đội: hướng dẫn git cơ bản (rebase, cherry-pick), hỗ trợ debug build khi cần.

## 3. SPEC mạnh/yếu

**Mạnh nhất:** Đảm bảo repo có quy trình rõ ràng và môi trường phát triển nhất quán, giảm thời gian on-boarding cho thành viên mới.

**Yếu nhất:** Chưa có CI/CD tự động đầy đủ (build/test/publish image), nên một số bước release vẫn thủ công và có thể gây lỗi người dùng.

## 4. Đóng góp khác
- Hỗ trợ các bạn trong nhóm với pull requests nhỏ, sửa lỗi Docker build và viết hướng dẫn chạy nhanh trong README.
- Giữ liên lạc với các thành viên để điều phối ai làm gì, ưu tiên task khi tiến độ bị chậm.

## 5. Điều học được
- Tầm quan trọng của branch discipline và review checklist để tránh regressions.
- Docker giúp tái tạo môi trường nhanh, nhưng cần automations (CI) để đảm bảo tính nhất quán.
- Task tracking rõ ràng giúp giảm friction khi phối hợp nhiều người trên cùng repo.

## 6. Nếu làm lại
- Thiết lập CI để tự động build, test và publish image khi merge vào main.
- Cấu trúc rõ ràng hơn cho issue templates và definition-of-done để giảm nhầm lẫn khi phân công task.

## 7. AI giúp gì / AI sai gì

**Giúp:** Dùng AI để draft mô tả PR, viết commit message tiêu chuẩn, gợi ý tối ưu Dockerfile và checklist release.

**Sai/mislead:** Đôi khi AI đề xuất workflow CI/CD quá phức tạp hoặc dùng công cụ ngoài phạm vi của dự án; cần cân nhắc trước khi áp dụng.

