# Bộ UAT automation Master 01

Bộ này chạy 35 case owner Gavin của `roles/qa/uat-master_1 (1).xlsx` (gọi tắt là master 01) trên môi trường host sẵn, mục đích là tìm defect. Bộ đi đúng các bước Steps và Expected của master 01, không theo luồng UAT chain (UAT-PRE, v4) của bộ `gavin_uat_automation`. Bộ cũ chỉ được dùng làm tài liệu tham khảo qua evidence (video, ảnh) để biết giao diện.

Màn hình và locator được lấy từ hai nguồn: evidence của bộ cũ, và DOM thật của e-Service, Admin Portal (MOE HQ và school) đọc ngày 31/10/2026. Các wizard MOEFAS, SBFAS, Top-up dùng id của phần tử (`#moefas-create-*`, `#sbfas-*`, `#top-up-*`), trang phụ huynh dùng aria-label (`View billing for <tên con>`, `Select charge: <tên phí>`).

## Cách chạy (Windows)

```
run_uat.cmd                                  chạy cả 35 case rồi xuất báo cáo
run_uat.cmd case UAT-PAR-01                  một case
run_uat.cmd case "UAT-PAR-01*,UAT-MOE-06"    nhiều case, phải có dấu nháy vì có dấu phẩy
run_uat.cmd group par                        một nhóm: moe, sch, par
run_uat.cmd case UAT-PAR-01 headed           xem trình duyệt chạy trực tiếp
run_uat.cmd report                           chỉ xuất lại báo cáo
```

`run_uat.cmd` dùng `.venv` của thư mục này, nếu không có thì dùng `.venv` của `gavin_uat_automation` hoặc `r4_automation`, nếu vẫn không có thì tự tạo và cài `requirements.txt`. Lần chạy đầu tự đọc master ra `data/master01_cases.json` bằng `tools/extract_master.py`.

Đăng nhập: phụ huynh qua Singpass simulator (chọn persona), MOE HQ và school qua nút Sign in with Microsoft rồi chọn ô tài khoản thử (admin@IAM.edu.vn, staff1@IAM.edu.vn). Không cần mật khẩu. Muốn dùng username và mật khẩu thì đặt `UAT_ADMIN_LOGIN=password`, `UAT_HQ_PASS`, `UAT_SCHOOL_PASS`.

## Kết quả của một bước và một case

| Kết quả | Ý nghĩa |
|---|---|
| PASS | mọi kiểm tra của bước đúng |
| PASS + EQUIV | chức năng có nhưng tên màn hình hoặc bố cục khác master (ví dụ Manage Budget là ô Total budget trong wizard). Ghi ở cột EQUIV của báo cáo. Đặt `UAT_STRICT_NAMES=1` để tính các bước này là GAP |
| FAIL | một kiểm tra sai (WRONG BEHAVIOUR) hoặc bước không thao tác được (ERROR, cần xem ảnh và video trước khi kết luận) |
| GAP | master mô tả màn hình, nút, trường mà bản build không có. Theo quy tắc 30/10/2026, GAP tính là FAIL |
| BLOCKED | bước không chạy được trên môi trường này: job chạy theo giờ, cần tech team giả lập, master thiếu dữ liệu, hoặc phụ thuộc bước trước không PASS |

Thứ tự ưu tiên của case: FAIL, GAP, BLOCKED, PASS. pytest báo FAIL và GAP là failed, BLOCKED là skipped.

## Đầu ra

```
artifacts/
  UAT_Master01_Report.xlsx   Summary (35 case), Defects (ứng viên defect kèm ảnh và video), Steps, Data mapping
  uat_summary.csv, uat_steps.csv
  results.json               kết quả thật từng bước: kiểm tra, GAP, EQUIV, lỗi API (HTTP >= 400) bắt được trong bước
  videos/<case>.webm         một video một case; case nhiều người dùng có <case>__parent, __school, __moe
  screenshots/<case>/        ảnh từng bước, tên có kết quả của bước
  discovery.json             kết quả quét persona trong ngày (con 16 tuổi, con PR, gia đình hai con chưa nộp đơn)
  run_state.json             mã đơn FAS và tên scheme do lần chạy tạo ra, để case sau dùng lại
```

Mỗi bước có thanh chữ in trên video: mã case, số bước, Expected của master, các kiểm tra, màu theo kết quả.

## Ánh xạ dữ liệu master sang môi trường

Master dùng `parent.test01`, `student.test01`, `EA-001`, `School Test 01` không có trên môi trường. Ánh xạ nằm ở `data/env_data.json`, mỗi case ghi lại ánh xạ đã dùng vào sheet Data mapping.

| Master | Môi trường |
|---|---|
| parent.test01, student.test01, EA-001 (thanh toán) | persona S8901234H (AHMAD BIN RAHMAN), con Ethan Rahman |
| EA balance 20.00 (N4, E2) | Leo Rahman, nạp 20.00 bằng HQ Individual Top-Up khi ví về 0 |
| phụ huynh SC có con 10 tuổi (FAS) | persona S7890123F (LIM WEI MINH), con Lucas Lim |
| parent.test99 | NRIC S0000999Z ở tab Password login của Singpass simulator |
| student.test16, student.pr01, hai con chưa nộp đơn | tìm tự động bằng cách quét mọi persona (discovery), không có thì BLOCKED |
| MOEFAS 2028, Tier 1 | tên kèm mã lần chạy để không trùng khi chạy lại |

## Dữ liệu bộ này tạo ra trên môi trường

Theo quyết định 30/10/2026 (đội tự tạo dữ liệu phí và top-up làm tiền điều kiện), bộ có thể: nạp tiền vào EA qua HQ Top-up (ghi chú `UAT master 01 precondition`), thanh toán phí của Ethan và Leo, tạo scheme MOEFAS và SBFAS có tên `UAT-...`, nộp đơn FAS cho con chưa có đơn. Bộ chỉ duyệt hoặc từ chối đơn do chính lần chạy tạo ra; muốn cho phép đơn khác thì đặt `UAT_ALLOW_FOREIGN_APPS=1` (không hoàn tác được từ giao diện). `UAT_NO_TOPUP=1` cấm nạp tiền, `UAT_NO_DISCOVERY=1` bỏ quét persona.

## Cấu trúc

```
conftest.py            fixture uat (một UatRun mỗi case), discovery, tùy chọn --uat-case
core/config.py         địa chỉ, tài khoản, tùy chọn UAT_*
core/recorder.py       UatRun: actor (cửa sổ và video riêng), step, check, gap, same_function, blocked, conclude
core/util.py           đọc tiền SGD, trạng thái dùng chung giữa các case
pages/auth.py          đăng nhập phụ huynh, MOE HQ, school
pages/eservice.py      Home, Edu Account, Pay education charges, cổng thanh toán giả lập, Invoices, Top-up, FAS
pages/admin.py         MOEFAS, FAS applications, Top-up, SBFAS, Pending allocations, Record a paper application
tests/test_01_moe.py ... test_05_par03.py   35 case, mỗi case một hàm test_UAT_xxx
tools/extract_master.py, tools/report.py
```

Quy tắc khi sửa: mỗi bước viết bằng `@uat.step(n, tiêu đề, expected)`, dùng `s.check(...)` thay cho `assert`, kết thúc case bằng `uat.conclude()`.
