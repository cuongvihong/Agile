# Phân tích coverage R9/R4, UAT Master, automation R9, và bắt đầu đối chiếu UI/FS/test case R9

## 1. Intro

Chat mới (session khác, không có context chat trước). Anh hỏi lần lượt nhiều việc trong cùng session: (a) repo GitHub `cuongvihong/Agile` lúc đầu trống, (b) test case hiện tại có cover đúng R9 và R4 không (lo ngại test case phụ thuộc UI flow), (c) phân tích file `uat-master.xlsx` (UAT Master), (d) đi sâu vào nhóm case Fees and payments của UAT Master, (e) automation R9 có cover hết test case không, (f) tìm file `r9_automation` (ban đầu tìm sai ở Drive, anh chỉnh lại là nằm trên GitHub), (g) các test automation R9 có tuân thủ đúng Test Steps của sổ case không, (h) bắt đầu đối chiếu UI thật (hai devtunnel admin portal 5173 và e-service 5174) với FS09 và sổ test case R9 để biết nên sửa test case thế nào.

## 2. Architecture

Phần việc này thuộc role QA/QA Lead, chạm vào: `roles/qa/r9_automation/` (automation Function 9), `roles/qa/R9_Test_Cases_final_FS09.xlsx` (sổ case R9), `roles/ba/FS09.md` và `roles/ba/[Agile] FS 09.docx` (functional spec), và UI thật của e-service/admin portal qua devtunnel. Không đụng code Dev, không đụng FS của BA.

## 3. Files modified

Không có. Toàn bộ task trong session này là đọc và phân tích, chưa sửa file nào trong repo.

## 4. Files added

- `session-process/2026-10-28_1523_phan-tich-r9-uat-coverage-va-ui-fs-check.md`: file này.
- Dòng mới trong Session Log của `CLAUDE.md` (xem mục riêng, theo Learned Rule 2026-09-20).

## 5. Files deleted

Không có.

## 6. Việc đã làm và phát hiện

### 6.1 Repo GitHub lúc đầu trống
Kiểm `git status`/`git log` trên `cuongvihong/Agile`: không branch, không commit. Sau đó trong lúc làm các việc khác, repo được push đầy đủ nội dung project lên `origin/main` (phát hiện qua `pushed_at` đổi khi gọi lại `list_repos`).

### 6.2 UAT Master (`uat-master.xlsx`, Google Drive, owner huyvu.workspace, không phải file của anh)
Đọc bằng openpyxl (không dùng snippet CSV lỗi dòng của công cụ Drive). 6 sheet: Tests, Timeline, Gates, Test data, Readiness, Team.
- Sheet Tests công bố "76 cases" nhưng đếm thật chỉ có 61 dòng case. READY-02 ghi số case theo người (Josh 18, Kent 13, Chan 15, **Howard 25**, Gavin 5 = 76) nhưng đếm thật Howard chỉ có 10 dòng → chênh đúng 15, toàn bộ nằm ở phần Howard.
- UAT-PAR-02 (+ 8 biến thể N1/N2/E1/E2/A1/N3/A2/N4) và UAT-PAR-01-E1 được Gate G3/G2 và assumption D05 liệt là "Affected tests" nhưng không có dòng nào trong sheet Tests.
- 61/61 case = Not Run. 4/4 Gate Open. 10 READY + 3 EXIT đều "Not checked" dù Timeline ghi hôm đó (28/10) là ngày chạy hết case.
- Quét từ khoá trong Steps: chỉ 21/61 (~34%) có nhắc cấp hệ thống (API/DB/job/webhook...), 36/61 chỉ diễn đạt bằng ngôn ngữ UI.

### 6.3 Nhóm Fees and payments trong UAT Master (9 case)
UAT-019, 020, 021, MOE-01 (Kent) và UAT-PAR-01 + 4 biến thể (Gavin). UAT-MOE-01 và UAT-PAR-01 còn treo ở gate "lifecycle" (Open); UAT-020/021/MOE-01 treo ở gate "school dates" (Open).
Phát hiện liên kết thật: UAT-PAR-01-N4 kỳ vọng "online fail thì hoàn phần EA" — đúng defect ưu tiên cao nhất mà QA ghi nhận khi chạy code Dev thật ngày 15/10/2026 (`roles/qa/F9_Dev_Local_Run_Results.md`): EA không được hoàn khi online thất bại. UAT-PAR-01-E2 cần "tech team simulate EA refund fail", ghi rõ UX hiện chưa có đường xử lý.

### 6.4 Automation R9 có cover hết sổ case không
Tìm đúng vị trí `roles/qa/r9_automation/` sau khi xác định không nằm ở Drive mà nằm trên GitHub (repo vừa được push). Đọc `README.md`, `docs/COVERAGE.md`, `docs/NOT_AUTOMATED.md`:
- Sổ case nguồn: `R9_Test_Cases_final_FS09.xlsx`, 187 case. 185 có test tự động (kể cả case gắn nhãn `known_defect`, `mocked`, `draft`). 2 case chưa tự động: TC-175 (thiếu dữ liệu tuổi con trên UI, chờ FS chốt rule R8), TC-204 (cần cách làm hỏng callback hợp lệ, ngoài phạm vi UI/API).
- Theo suite: chỉ F9.1 (thiếu TC-175) và F9.6 (thiếu TC-204) có 1 case chưa tự động, còn lại 100%.
- "Đã cover" không đồng nghĩa "đã Pass": 75 test `known_defect` (xfail có chủ đích), 35 `draft` (phụ thuộc assumption mở), 38 `mocked`.
- Bộ case gốc (153 case, trước khi thêm 34 case `rules` ngày 25/10) đã chạy thật 2 lần trên hệ thống local: lần 2 — 64 Pass, 1 Fail (đã sửa), 0 Error, 97 Skip, 20 known_defect đúng kỳ vọng. 34 case rules mới chỉ `pytest --collect-only`, chưa chạy thật.

### 6.5 Automation có tuân thủ đúng Test Steps của sổ case không
Đối chiếu trực tiếp cột Test Steps/Expected Result của `R9_Test_Cases_final_FS09.xlsx` với docstring + assert thật trong code (không dựa vào tên hàm):
- 5 case mẫu khớp qua nhiều suite khác nhau (TC-001, TC-018, TC-065, TC-097, TC-173 — thuộc F9.1, F9.2, F9.4, F9.5, F9.9): nội dung code đúng với Test Steps/Expected.
- **Phát hiện lệch thật trong `tests/test_f96_webhook_and_reconciliation.py`**: số TC trong tên hàm (cũng là số mà `tools/build_coverage.py` dùng để dựng `docs/COVERAGE.md`) không khớp nội dung hiện hành của sổ case cho đúng số đó:
  - Hàm `test_tc_111_...` (nội dung: webhook thiếu signature bị 401) ↔ đúng là nội dung của **TC-113** trong sổ hiện hành.
  - Hàm `test_tc_113_...` (nội dung: webhook bị sửa sau khi ký) ↔ đúng là nội dung của **TC-114**.
  - Hàm `test_tc_115_...` (nội dung: webhook hợp lệ lưu đủ metadata, Processed) ↔ đúng là nội dung của **TC-111**.
  - Hàm `test_tc_119_...`, `test_tc_120_...` cũng lệch so với tiêu đề TC-119/TC-120 mà `docs/COVERAGE.md` tự sinh từ sổ case.
  - Suy luận: tàn dư từ lần đổi số case cũ (FS09 final bỏ 19 case, đổi số — đã ghi trong Session Log 22/10), riêng file `test_f96` chưa được khớp lại theo số mới. Chỉ phát hiện trong `test_f96`; 5 file suite khác đã kiểm mẫu không thấy lệch kiểu này, nhưng chưa rà toàn bộ 187 case nên không khẳng định các file khác hoàn toàn sạch.

### 6.6 Bắt đầu đối chiếu UI thật / FS / test case R9 — BLOCKED
Anh đưa 2 link devtunnel: `https://hvsxj426-5173.asse.devtunnels.ms/` (Admin Portal) và `https://hvsxj426-5174.asse.devtunnels.ms/` (E-Service). Thử `WebFetch` cả hai, bị chặn bởi network policy của session cloud (`ENOTFOUND`). Anh nói đã cho phép domain, thử lại vẫn `ENOTFOUND` như cũ. Kiểm `roles/dev/` trong repo: chỉ có tài liệu (Database Design, Sprint Backlog, 2 PDF luồng xác thực, DataTest.zip), **không có source code frontend (.tsx) nào được commit** nên không có cách đọc UI thật thay thế ngoài việc chờ devtunnel mở được. Nguồn gần nhất hiện có: `roles/qa/r9_automation/data/ui_text.py` (câu chữ UI chép lại, có thể cũ) và ảnh chụp thật màn A→D (21/10) trong `roles/qa/R9_FAS_Validation_Rules.docx` (màn E→G chỉ là sơ đồ QA vẽ, chưa chụp được).

## 7. Skills used

- `qa-course:working-protocol`: đọc lại `references/working-protocol.md` đầy đủ để ghi Session Log và file session-process đúng quy trình (mục 8), theo yêu cầu "lưu session log" của anh.

## 8. External references

- Google Drive: `qa.md`, `qalead-2-workbook.md` (bản đồ role qa/qalead), `2026-10-19_2336_r4-compare-va-test-case.md`, `2026-10-15_0720_chay-kich-ban-function9-localhost.md`, `uat-master.xlsx` (file của huyvu.workspace, không phải của anh).
- GitHub: `cuongvihong/Agile` (repo chính của project, đọc trực tiếp sau khi được push), `cuongvihong/aiqa` (gắn nhầm lúc đầu, không liên quan — là project automation khác, "curricula_trainer_account").

## Còn mở

- Chờ devtunnel `*.asse.devtunnels.ms` truy cập được từ session (có thể cần session mới sau khi đổi Network access, không áp dụng ngược cho session đang chạy) để tiếp tục đối chiếu UI thật với `roles/ba/FS09.md` và `R9_Test_Cases_final_FS09.xlsx`.
- Anh cần quyết có sửa lại số TC lệch trong `test_f96_webhook_and_reconciliation.py` (ít nhất TC-111, 113, 114, 115, 119, 120) không, và có cần rà toàn bộ 187 case thay vì chỉ mẫu 5 case không.
- Session Log của `CLAUDE.md` hiện có rất nhiều dòng không ghim (ước khoảng 29) vượt xa giới hạn 5 dòng — có vẻ việc xoay vòng đã bị bỏ sót nhiều phiên liên tiếp. Chưa tự xử lý backlog này, đã báo riêng cho anh quyết.
