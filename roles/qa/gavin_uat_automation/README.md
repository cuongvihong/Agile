# Bộ UAT Gavin: chạy thật luồng UAT, quay video từng bước

Bộ này thay bộ cũ. Bộ cũ chỉ mở vài trang rồi báo Passed cho cả 35 case nên kết quả không có giá trị.
Bộ mới bám 35 case của `roles/qa/uat-master_1 (1).xlsx` (các cột Steps, Expected, Setup, Gate) và làm đúng các việc sau:

1. Mỗi case chạy từng bước của master trên bản build thật ở **localhost**. Không chạy Vercel.
2. Mỗi người dùng (phụ huynh, trường, MOE HQ) có **một cửa sổ riêng và một video riêng**. Video lưu tại `artifacts/videos/<case>.webm`, nếu case có nhiều người dùng thì `<case>__parent.webm`, `<case>__school.webm`, `<case>__moe.webm`.
3. **Mỗi bước có thanh chữ in thẳng vào video** ở đáy màn hình: mã case, số bước, việc đang làm, Expected của master, các kiểm tra đã làm. Thanh đổi màu khi bước xong: xanh PASS, đỏ FAIL, cam BLOCKED, tím GAP.
4. Mỗi bước có ảnh chụp `artifacts/screenshots/<case>/NN-<bước>-<kết quả>.png` và một step trong Allure.
5. Kết quả thật của từng case nằm trong `artifacts/uat_results.json`, xuất ra CSV bằng `tools/export_results.py`.

## Bốn kết quả của một case (không có đạt giả)

| Kết quả | Ý nghĩa | pytest |
|---|---|---|
| PASS | Mọi bước chạy và mọi kiểm tra đúng | passed |
| FAIL | Một kiểm tra sai hoặc không thao tác được. Bằng chứng ở video và ảnh | failed |
| BLOCKED | Bước không chạy được trên môi trường này (job chạy theo giờ, cần tech giả lập, thiếu dữ liệu, master không cho giá trị) | skipped |
| GAP | Master mô tả màn hình hoặc nút mà bản build không có. Màn hình thật được chụp để chứng minh. Từ 30/10/2026 anh đã duyệt GAP tính là FAIL, nên case có bước GAP kết thúc là FAIL (bước vẫn hiện nhãn GAP để phân biệt với lỗi chạy) | failed |

Thứ tự ưu tiên khi một case có nhiều loại: FAIL, rồi GAP, rồi BLOCKED, rồi PASS.

Ô tick "also consider SBFAS" của master không còn là yêu cầu (client xác nhận 30/10/2026: khi trượt MOEFAS hồ sơ tự chuyển sang SBFAS của trường). Bộ test chỉ ghi chú điều này, không tính là lỗi.
Một case chỉ PASS khi **tất cả** các bước PASS.

## Cách chạy (Windows)

Cần stack localhost đang chạy: Admin Portal 5173, e-Service 5174, payment checkout simulator 5176 (nhóm thanh toán), Docker container `edufams-qa-sqlserver` (nhóm thanh toán và MOE-01).

```
run_uat.cmd                      chạy hết 35 case
run_uat.cmd case UAT-PAR-01      một case (cho phép dấu *: UAT-PAR-*, UAT-MOE-05*)
run_uat.cmd group par            một nhóm: par, moe, sch
run_uat.cmd case UAT-PAR-01 headed   xem trình duyệt chạy trực tiếp
run_uat.cmd report               chỉ xuất CSV từ lần chạy trước
```

Hoặc gọi pytest trực tiếp từ thư mục này: `python -m pytest --uat-case "UAT-MOE-*" --alluredir artifacts\allure-results`.
`run_uat.cmd` dùng `.venv` của thư mục này, nếu không có thì dùng `..\r4_automation\.venv`, nếu cả hai không có thì tự tạo `.venv`.

Biến môi trường tùy chọn: `UAT_ADMIN_URL`, `UAT_PARENT_URL`, `UAT_CHECKOUT_URL`, `UAT_SLOW_MO` (ms giữa các thao tác, mặc định 250), `UAT_STEP_PAUSE` (ms dừng sau mỗi bước để đọc thanh chữ, mặc định 1200), `UAT_NO_DB=1` (không dùng Docker, các case cần DB thành BLOCKED), `UAT_HQ_USER` và `UAT_HQ_PASS`, `UAT_SCHOOL_USER` và `UAT_SCHOOL_PASS`, `UAT_PARENT_NRIC`.
Địa chỉ mặc định của bộ là môi trường host sẵn (Admin https://admin.20-255-158-192.sslip.io, e-Service https://eservice.20-255-158-192.sslip.io), `run_uat.cmd` chạy thẳng trên đó và tự tắt phần dùng Docker/DB. Muốn chạy localhost thì đặt `UAT_ADMIN_URL=http://localhost:5173` và `UAT_PARENT_URL=http://localhost:5174`. Nhóm thanh toán cần thêm `UAT_CHECKOUT_URL` của simulator thanh toán trên host, nếu không sẽ BLOCKED. Không có Docker nên các case cần đổi số dư ví hay khoản phí bằng SQL sẽ BLOCKED. Bộ từ chối chạy khi địa chỉ không phải localhost, trừ host nằm trong `UAT_ALLOW_HOSTS`. Máy trong mạng riêng của bạn chỉ được dùng khi đặt `UAT_ALLOW_REMOTE=1`. Địa chỉ vercel.app bị chặn hẳn.

## Kết quả đầu ra

```
artifacts/
  videos/                  video webm của từng case và từng người dùng
  screenshots/<case>/      ảnh từng bước, tên có kết quả của bước
  uat_results.json         kết quả thật: từng case, từng bước, kiểm tra, lý do BLOCKED hoặc GAP
  uat_summary.csv          một dòng một case (sau run_uat.cmd report)
  uat_steps.csv            một dòng một bước
  allure-results/          dữ liệu Allure (có video và ảnh gắn vào từng bước)
```

`uat_results.json` giữ kết quả lần chạy gần nhất của mỗi case, có cột `ran_at`. Case nào chưa chạy lại vẫn mang kết quả cũ.

## Ánh xạ dữ liệu master sang dữ liệu thật của stack

Master dùng `student.test01`, `EA-001`, `S0000001A`, `School Test 01`. Các dữ liệu này không có trên stack. Bộ dùng seed R9 đang có:

| Master | Stack thật |
|---|---|
| student.test01 / EA-001 (ví, hóa đơn) | R9 Sandbox Teo (R9-STU-14, EDU-01044), khoản phí tạm và số dư đặt bằng `pages/db.py` rồi dọn lại cuối case |
| student.test16 | R9 Teen Yeo (R9-STU-10) |
| con có hai hóa đơn đã trả | R9 Paid Koh (R9-STU-07) |
| parent.test01 | persona Singpass S7890123F (chủ các con R9) |
| phụ huynh có hai con | persona S9123456J (Ella Smith, Isabella Smith) |
| Tier 1, MOEFAS 2028 | tên `UAT-GAVIN-<mã>-<giờ>` và kỳ xa trong tương lai để chạy lại không trùng |

Seed R9 phải đã nạp (`tools/seed_r9_data.sql`). Nếu cần nạp lại: `python -c "from pages import db; db.reseed()"`.

## Dự đoán trước lần chạy thật đầu tiên

Tôi chưa chạy bộ này trên stack của bạn (môi trường của tôi không với tới localhost của bạn). Tôi chỉ kiểm tra biên dịch, `pytest --collect-only` (35 case) và chạy thử bộ ghi video, thanh chữ, ảnh, JSON trên một trang mẫu. Đây là dự đoán từ mã nguồn, **kết quả thật là file `uat_results.json` sau khi bạn chạy**:

**Chạy trọn luồng, có thể PASS hoặc FAIL thật (8 case):** UAT-PAR-01, PAR-01-N1, N2, E1, N3, A1, N4 và MOE-06-N1.

**Chạy xong nhưng sẽ là GAP vì master mô tả thứ build không có (14 case):**
- PAR-02, N1, N2, E1, E2: build có một form FAS duy nhất, không có wizard 5 bước, không có nháp, không có kiểm tra "form đang mở" ở màn chọn con, không có danh sách con bị khóa.
- PAR-03, A1: trang Invoices & payments không có dòng Money in, Home không có khối Recent EA activity.
- MOE-04, MOE-05, SCH-04: không có màn Manage Budget riêng và không có trang Budget Tracking riêng. Ngân sách là ô Total budget ở bước General và thẻ ở tab Statistics. Các bước tương đương vẫn được chạy.
- MOE-06: GAP nếu danh sách scheme không hiện chữ Approved automatically.
- SCH-01, N1, E1: trường học không có màn Upload applications, Upload scans, Review application. Bộ mở menu FAS applications của trường để chụp bằng chứng, nếu sau này build có màn này thì case chuyển thành BLOCKED để bạn rà bằng tay.

**BLOCKED (12 case):**
- Job đồng bộ hằng ngày không chạy được từ giao diện: MOE-01 (và việc tạo trường, lớp, học sinh vì master không cho giá trị). Phần phụ huynh thấy khoản phí 100.00 được chạy thật.
- Cần tech giả lập lỗi hoàn tiền: PAR-01-E2.
- Quyết định MOEFAS chạy theo giờ sau khi form đóng, phê duyệt của trường, thiếu đơn Pending: PAR-02-A1, A2, N3, N4, SCH-03, SCH-03-N1. Bộ cố ý không duyệt hay từ chối đơn thật vì không hoàn tác được từ giao diện.
- Ngân sách đã cạn cần job cấp trợ cấp: MOE-05-E1, SCH-04-E1. Bộ vẫn tìm scheme đã cạn, nếu có thì kiểm cảnh báo. Bước cấp thêm trợ cấp là BLOCKED, và R6 đã ghi BUG-R6-003 (build chặn cấp vượt ngân sách, ngược với master).
- PAR-03-E1: master mô tả trạng thái trước khi có danh sách, build đã có Invoices & payments.
- SCH-02: bước cuối "trợ cấp áp dụng cho học sinh đã được cấp" cần học sinh đang giữ scheme. Các bước trước vẫn chạy thật.

**Dự đoán FAIL thật (1 case):** SCH-02-N1. Build từ chối scheme trùng tên và kỳ nhưng thông báo không nói về overlap. R4 đã ghi lỗi này (TC-222b).

## Dữ liệu bộ này tạo ra

- Phí tạm và số dư ví cho R9 Sandbox Teo: tự dọn cuối mỗi case. Nếu máy tắt giữa chừng, chạy lại `reseed`.
- Scheme MOEFAS: giao diện không xóa được. Tên bắt đầu bằng `UAT-GAVIN-`. Dọn bằng `tools/cleanup_uat_schemes.sql` (soft delete).
- Scheme SBFAS bản nháp: bộ tự xóa bằng API. Bản đã Publish giữ lại, dọn cùng file SQL ở trên.

## Cấu trúc

```
conftest.py                  fixture uat (video, thanh chữ, kết quả), tùy chọn --uat-case
uat/env.py                   địa chỉ, tài khoản, nhịp quay, chốt chặn chỉ localhost
uat/recorder.py              UatRun: actor, step, check, blocked, gap, conclude
uat/actors.py                đăng nhập Singpass (phụ huynh), đăng nhập Admin Portal
uat/flows.py                 dữ liệu chuẩn bị bằng DB, thẻ Home, đi qua simulator thanh toán
uat/admin_flows.py           đọc thẻ ngân sách, tìm scheme đã cạn, mở tab Statistics
pages/                       page object (billing, accounts, result, simulator, FAS form, MOEFAS, SBFAS, API)
data/uat_cases_meta.py       Steps và Expected của 35 case, lấy từ uat-master
tests/test_uat_par_01_payments.py, test_uat_par_02_fas.py, test_uat_par_03_activity.py
tests/test_uat_moe.py, test_uat_sch.py
tools/                       export_results.py, cleanup_uat_schemes.sql, seed R9
```

## Quy tắc khi sửa bộ này

- Mỗi test kết thúc bằng `uat.conclude()`. Không dùng `assert` rời, dùng `uat.check(...)` để lỗi hiện lên thanh chữ và ảnh.
- Chỉ dùng `uat.gap(...)` khi đã thấy trên màn hình rằng build không có thứ master mô tả. Chỉ dùng `uat.blocked(...)` khi bước thật sự không chạy được, và ghi lý do.
- Không gắn cứng kết quả. Nếu build sau này có tính năng, case tự chuyển sang chạy thật hoặc sang BLOCKED để rà tay.

## Precondition: du lieu top-up, phi va FAS (UAT-PRE-01, UAT-PRE-02, UAT-PRE-03)
Host Azure khong reset duoc nen bo UAT tu tao data: `tests/test_uat_pre_seed.py` chay TRUOC moi lan chay UAT (ke ca khi chon `case` hoac `group`), co video, banner va anh tung buoc nhu cac case khac.
- UAT-PRE-01: top-up SGD 20 cho Ethan Rahman, Leo Rahman, Isaac Chen; chien dich "UAT-SEED Bulk 20 age 10" (khong chay). Doc lai o Top-Up History va danh sach chien dich.
- UAT-PRE-02: khoan phi UAT-SEED Fee 100, 600, 50 voi muc gia (PRIMARY, SC), dot phat hanh cho hoc sinh chon, cho den khi Completed; sau do phu huynh dang nhap va thay khoan phi tren man hinh thanh toan.
- Tao bang API cua Admin (cung loi goi cua man hinh) voi cookie cua cua so MOE HQ; ket qua luon doc lai tren man hinh.
- Cong them, khong xoa, chay lai an toan: `artifacts\seed_state.json` nho muc da tao. Log lenh goi: `artifacts\seed_log.jsonl`.
- `run_uat.cmd seed` chay rieng; `UAT_SEED=0` bo qua; `UAT_SEED=plan` chi doc; `UAT_SEED_RUN_CAMPAIGN=1` chay chien dich.
- Doi hoc sinh, so tien, ten: sua `data/seed_plan.py`. Case UAT lay hoc sinh da seed bang `uat.seed.seeded_students()`.
- UAT-PRE-03 (FAS): dung scheme MOEFAS THAT, khong tao scheme moi. Ly do: API va man hinh deu chan scheme trung khoang thoi gian (form 01/01/2026 den 11/30/2026, hieu luc 12/01/2026 den 12/31/2027 da phu het), nen khong tao duoc scheme gan han.
  Buoc 1 R6: HQ mo man hinh MOEFAS, doc ngan sach (tong, da dung, con lai). Ngan sach 0 se ghi BLOCKED vi confirm se bi INSUFFICIENT_BUDGET, scheme da tao chi xem duoc nen Dev/BA phai dat ngan sach.
  Buoc 2 R10: phu huynh S8901234H (Ahmad Bin Rahman) nop don cho Ethan va Leo bang loi goi cua form (prefill roi POST), lan sau tim thay don thi khong nop lai. Con phai la hoc sinh that cua phu huynh, nen khong dung Isaac/Sophia (da Approved APP-01003) va Lim/Pham/Bui (da co don Pending).
  Buoc 3: HQ thay 2 allocation Pending cua don moi. Buoc 4: HQ chi confirm duoc TU ngay hieu luc cua scheme (12/01/2026); truoc ngay do ghi BLOCKED, tu ngay do chay lai `run_uat.cmd seed` la buoc nay tu duyet (preview roi confirm, chi allocation cua don seed). Buoc 5: phu huynh thay Approved.
  Buoc 6 R5 (don giay tai truong): chua tu dong hoa, ghi BLOCKED; nhap tay tren man hinh truong cho be chua co don.


## Dong bo voi uat-master.xlsx ngay 30/10/2026 (Sprint 3 UAT, 61 case)
Cac buoc cua UAT-PAR-01, PAR-01-N3, PAR-01-A1, PAR-01-N4, PAR-01-E2 doi theo master moi (`data/uat_master_v3.py`, gop vao `data/uat_cases_meta.py`). Them hai case moi UAT-031 va UAT-033 trong `tests/test_uat_fas_assessment.py`.
Du lieu seed duoc phep khac master mien buoc giong: moi case thanh toan co be va khoan phi rieng de case nay khong an du lieu cua case kia (bang `PAY_CASES` trong `data/seed_plan.py`).
Seed hien co: Fee 100 (Ethan, Leo), Fee 600 (Isaac, Grace, Leo), Fee 50 (Grace, Sophia). Master dung EA 100 hoac 20 va hoa don 50, seed dung so tien khac nhung cung cac buoc. Case ghi chu chenh lech so tien trong ket qua.
Thanh toan thanh cong tieu du lieu seed. Chay thanh toan lan hai: dat `UAT_SEED_ROUND=2` roi `run_uat.cmd seed` (them hau to r2 vao ten khoan phi, nap lai khoan phi moi).
UAT-031: buoc 1 tao ban nhap qua wizard roi doc lai tu server; buoc 2 server tu choi ngay hieu luc bang ngay dong don va ngan sach 0 khi publish; buoc 3 publish roi scheme chi doc. Con BLOCKED: School B (moi truong chi co 1 user truong), bang ky vong voi Gavin va trigger (G3, D06).
UAT-033: buoc 1 luu ma tran tro cap 50 phan tram cho khoan phi duoc ho tro, doc lai, khoan khong chon khong co trong ma tran. Buoc 2 den 4 BLOCKED vi tro cap chi ap vao khoan phi cua hoc sinh sau khi don duoc duyet, ma duyet chi lam duoc tu ngay hieu luc cua scheme (scheme moi nam xa trong tuong lai).
Van BLOCKED sau khi dong bo: PAR-01-A1 (khong co cong cu QA phat lai thong bao da settle), PAR-01-N4 (simulator khong co huy hay timeout mo ho), PAR-01-E2 (can doi ky thuat), doi chung khoan phi da huy trong PAR-01 (chi ghi chu).
Chua chay that tren host: UAT-PRE-03, nhom PAR-01, UAT-031, UAT-033. Chay `run_uat.cmd seed headed` roi `run_uat.cmd case "UAT-PAR-01*"` va `case "UAT-031,UAT-033"`, gui lai `artifacts\seed_log.jsonl`, `uat_results.json`, `uat_summary.csv`.


Pham vi chay mac dinh: `run_uat.cmd hosted headed` chi chay 3 case seed va 7 case co Owner la Gavin trong uat-master (UAT-PAR-01, A1, E2, N3, N4, UAT-031, UAT-033). `run_uat.cmd all hosted` chay het cac case con lai cua bo.


Cap nhat 31/10/2026: build chua co chuc nang hoan EA, doi soat hoan tay (xac nhan cua nhom). UAT-PAR-01-N4: khi phan online that bai, he thong chuyen sang 'Payment needs review', EA khong duoc hoan tu dong. Test kiem phan he thong lam duoc (phi bi giu, EA chi bi tru mot lan) va ghi GAP 'NOT IN BUILD' cho viec hoan EA va hoa don ve Issued. UAT-PAR-01-E2 chay that tren be rieng (Leo, UAT-SEED Fee 700, EA 520 cong online 180, cong thanh toan gia lap Failed): trang 'Payment needs review', phu huynh thay trang thai xac minh, phi bi giu; canh bao cho van hanh ghi BLOCKED vi QA khong thay.


Vong seed tu 2 tro di (UAT_SEED_ROUND=2) con tu nap lai EA cho Ethan, Leo, Isaac, Grace ve 520 (UAT-PRE-01, moi lan toi da 100), vi thanh toan thanh cong hoac bi giu doi soat da dung het EA. Neu nguoi doi soat hoan tay EA cho cac be nay thi so du co the vuot 520 va UAT-PAR-01-N3, N4 se khong con dung dieu kien (phi 600 phai lon hon EA).


Quyet dinh ngay 31/10/2026 (Cuong): UAT-PAR-01-A1 buoc 5 (phat lai thong bao settle cua cong) bo khoi case vi QA khong co cong cu, thay bang buoc thuc te hon: mo lai trang 'Payment successful' va bam Pay lan nua tren cung phien cong, roi kiem khong tru EA lan hai, khoan phi khong tra lai duoc, lich su co dung mot hoa don. Buoc nay yeu hon viec phat lai thong bao that cua cong, ghi ro trong ket qua. Neu sau nay Dev cap cong cu phat lai thi them lai buoc goc.

## Receipt: no invoice status check (31 Oct 2026)
The two GAP rows "Invoice status on the receipt" are removed from UAT-PAR-01 and UAT-PAR-01-A1. The tests now check only the fields the build receipt has: invoice number, issued at, completed at, gross amount, subsidy, amount due, payment method (helper `_check_receipt_fields`). Paid is read from the result "Payment successful" and from the fee leaving the pay list.
- 2026-10-31: Gavin tests aligned to the current UI and the v4 chain design. PAR-01 7 steps, N3 two charges, A1 child 1 Both and child 2 online, N4 passes only when Payment failed shows the reversal (today GAP: Payment needs review), E2 expects Payment needs review. FAS file rewritten: 031 compares HQ FAS applications with the MOEFAS rule, new 031-E1 (Not approved to school Pending School Review), 033 reads Gross, Subsidy, Amount due (BLOCKED before 1 Dec 2026). Compiled and collected only, not run on the host.
- 2026-10-31: run_uat.cmd tu tang UAT_SEED_ROUND (artifacts\seed_round.txt, bat dau 6), mot lenh .\run_uat.cmd hosted headed seed truoc roi chay 8 case Gavin.
- 2026-10-31: UAT-PAR-01-N4 aligned to the client rule (no automatic refund, Payment needs review, system check then manual reconciliation). Steps 1 and 2 pass on that state, manual reconciliation and cancel/timeout stay BLOCKED.

- 31/10/2026: them UAT-PRE-04 (tao School B UATB01 va school user qua API cua Admin, khong ghi mat khau), phi UAT-SEED Fee S100 cho Sophia (UAT-033), danh sach phi cua e-Service phan trang 10 dong nen script doc het cac trang (billing_page.read_all_charges, reveal).

FAS form (e-Service): the form opens with the children and the spouse of the parent filled from system records and locked, plus a required Employment status. The tests replace the locked children by typed rows (use_only_typed_beneficiaries). UAT-PAR-02-A2 searches all Singpass personas for a PR; UAT-SCH-01 family saves the controls of Record a paper application in artifacts/probe_*.json.
