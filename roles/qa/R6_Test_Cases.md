# TÀI LIỆU TEST CASES: REQUIREMENT R6 – FAS BUDGET & STATISTICS

> **Dự án:** EduFAMS (Agileproject - Hệ thống Quản lý Tài chính Giáo dục MOE Singapore)
> **Requirement:** R6 – FAS Budget & Statistics (R6.1 Budget Management, R6.2 Subsidy Statistics, R6.3 Budget Tracking)
> **Tài liệu căn cứ:** `roles/ba/FS06.md` (v0.1 Draft) đối chiếu `roles/ba/FS04.md` và `roles/qa/R6_FAS_Validation_Rules.md`
> **Tổng số Test Cases:** 56 ca kiểm thử (Bao gồm các ca Approve, Draft kèm giả định mở ASM-R6-xx, và Block do mâu thuẫn FS04)

---

## Test Suite: F6.1 Access & Authorization

### [TC-001] MOE HQ User accesses national MOEFAS budget management view

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-001` |
| **Test Suite** | `F6.1 Access & Authorization` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-13` |
| **Truy vết (Traceability)** | `FS06: 1.2, 5.1.3, BR6.01, R6-02` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Active MOE HQ user exists in IAM (moehq / Mei Lin Tan).
- 2. User is signed in to Admin Portal.

**2. Dữ liệu kiểm thử (Test Data):** `User: Mei Lin Tan (moehq), Scheme: MOEFAS`

**3. Các bước thực hiện (Test Steps):**
1. Open Admin Portal.
2. Navigate to budget management view (menu name to be confirmed when built).
3. Observe page view and FAS scheme.

**4. Kết quả mong đợi (Expected Result):**
1. MOE HQ user successfully accesses budget management view.
2. FAS Type displays 'MOEFAS' as read-only label.
3. Budget amount input field is accessible for configuration.

> [!NOTE]
> **Ghi chú:** Navigation path provisional until UI built.

---

### [TC-002] MOE HQ User views national MOEFAS budget without school restrictions

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-001` |
| **Test Suite** | `F6.1 Access & Authorization` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 1.2, BR6.01, R6-02` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ User (Mei Lin Tan).

**2. Dữ liệu kiểm thử (Test Data):** `Scheme: MOEFAS`

**3. Các bước thực hiện (Test Steps):**
1. Open MOEFAS budget management view.
2. Check scope indicators.

**4. Kết quả mong đợi (Expected Result):**
1. View displays national scheme-level scope.
2. User is not locked to or restricted by any specific school ID.

> [!NOTE]
> **Ghi chú:** HQ national scope confirmation.

---

### [TC-003] School User accesses SBFAS budget view pre-populated with assigned school

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-002` |
| **Test Suite** | `F6.1 Access & Authorization` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 1.2, 5.2.3, BR6.01, R6-03` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. School Admin signed in (Bukit View Primary School, Lan Nguyen).

**2. Dữ liệu kiểm thử (Test Data):** `User: Lan Nguyen, School: Bukit View Primary School (BVP-0012)`

**3. Các bước thực hiện (Test Steps):**
1. Open budget management view.
2. Inspect displayed School name and FAS Type.

**4. Kết quả mong đợi (Expected Result):**
1. Page displays School name 'Bukit View Primary School' as read-only text.
2. FAS Type displays 'SBFAS' as read-only text.
3. School user cannot change the school name.

> [!NOTE]
> **Ghi chú:** School Admin scoped access.

---

### [TC-004] School User calling SBFAS API with another school ID receives 403 Forbidden

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-003` |
| **Test Suite** | `F6.1 Access & Authorization` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Security` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 1.2, BR6.01, R6-09` |
| **Môi trường (Environment)** | API Gateway: http://localhost:5273 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Authenticated as School Admin of Bukit View Primary (BVP-0012).

**2. Dữ liệu kiểm thử (Test Data):** `Assigned School: BVP-0012, Target School: MRS-0012 (Meridian Secondary)`

**3. Các bước thực hiện (Test Steps):**
1. Send API GET or POST request to SBFAS budget endpoint supplying schoolId = 'MRS-0012'.
2. Inspect HTTP status code and response body.

**4. Kết quả mong đợi (Expected Result):**
1. API rejects request with HTTP 403 Forbidden.
2. Response body contains message: 'Access denied. You do not have permission to access or modify this budget record.'

> [!NOTE]
> **Ghi chú:** Data isolation boundary enforcement.

---

### [TC-005] School User calling MOEFAS budget API receives 403 Forbidden

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-003` |
| **Test Suite** | `F6.1 Access & Authorization` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Security` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 1.2, BR6.01, R6-02` |
| **Môi trường (Environment)** | API Gateway: http://localhost:5273 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Authenticated as School Admin (Lan Nguyen).

**2. Dữ liệu kiểm thử (Test Data):** `Endpoint: /api/fas/v1/budgets/moefas`

**3. Các bước thực hiện (Test Steps):**
1. Send POST/PUT request to MOEFAS budget endpoint with valid payload.
2. Inspect response status code.

**4. Kết quả mong đợi (Expected Result):**
1. API rejects request with HTTP 403 Forbidden.
2. School Admin is prohibited from modifying MOEFAS national budget.

> [!NOTE]
> **Ghi chú:** Cross-role security boundary.

---

### [TC-006] MOE HQ User calling SBFAS school budget API directly receives 403 Forbidden

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-003` |
| **Test Suite** | `F6.1 Access & Authorization` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Security` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 1.2, BR6.01, R6-03` |
| **Môi trường (Environment)** | API Gateway: http://localhost:5273 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Authenticated as MOE HQ (Mei Lin Tan).

**2. Dữ liệu kiểm thử (Test Data):** `Endpoint: /api/fas/v1/budgets/sbfas, SchoolId: BVP-0012`

**3. Các bước thực hiện (Test Steps):**
1. Send POST/PUT request to set SBFAS budget for BVP-0012 directly.
2. Inspect response status code.

**4. Kết quả mong đợi (Expected Result):**
1. API rejects request with HTTP 403 Forbidden.
2. MOE HQ cannot override individual school SBFAS budget without delegation.

> [!NOTE]
> **Ghi chú:** HQ to School boundary isolation.

---

### [TC-007] Unauthenticated user redirected to login when accessing budget routes

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-003` |
| **Test Suite** | `F6.1 Access & Authorization` |
| **Giao diện (Page)** | `Login Page` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Security` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-13` |
| **Truy vết (Traceability)** | `FS06: 5.1.2, 5.2.2` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Browser session has no JWT token or authentication cookie.

**2. Dữ liệu kiểm thử (Test Data):** `URL: http://localhost:5173/fas-budget-management`

**3. Các bước thực hiện (Test Steps):**
1. Directly input budget management URL into browser address bar.
2. Press Enter.

**4. Kết quả mong đợi (Expected Result):**
1. System redirects immediately to login page.
2. No budget data or dashboard elements are rendered.

> [!NOTE]
> **Ghi chú:** Route guard check.

---

## Test Suite: F6.2 MOEFAS Budget Setup

### [TC-008] Configure MOEFAS budget with valid whole number amount

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.1.4, AC-R6.1.1, R6-04` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ (Mei Lin Tan).
- 2. MOEFAS budget configuration form open.

**2. Dữ liệu kiểm thử (Test Data):** `Budget Amount: 5000000`

**3. Các bước thực hiện (Test Steps):**
1. Enter 5000000 into Budget Amount input field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Budget amount is saved successfully.
2. System displays confirmation message: 'Budget amount has been successfully configured and saved.'
3. Configured Budget Amount displays 'S$ 5,000,000.00'.

> [!NOTE]
> **Ghi chú:** Happy path integer budget.

---

### [TC-009] Configure MOEFAS budget with valid 2-decimal places (cents)

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.1.4, R6-04` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.
- 2. Form open.

**2. Dữ liệu kiểm thử (Test Data):** `Budget Amount: 7500000.50`

**3. Các bước thực hiện (Test Steps):**
1. Enter 7500000.50 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Budget is saved successfully.
2. Configured Budget Amount displays 'S$ 7,500,000.50'.

> [!NOTE]
> **Ghi chú:** Valid decimal cents input.

---

### [TC-010] Configure MOEFAS budget with 0.00 as valid initial allocated budget

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.1.4, BR6.03, R6-04` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Budget Amount: 0.00`

**3. Các bước thực hiện (Test Steps):**
1. Enter 0.00 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Budget amount 0.00 is accepted and saved.
2. Configured Budget Amount displays 'S$ 0.00'.

> [!NOTE]
> **Ghi chú:** Zero budget valid initial state.

---

### [TC-011] Validation error when MOEFAS Budget Amount is left empty

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.1.3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.
- 2. Budget Amount field cleared.

**2. Dữ liệu kiểm thử (Test Data):** `Budget Amount: (empty)`

**3. Các bước thực hiện (Test Steps):**
1. Leave Budget Amount field empty.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Save operation is blocked.
2. Field validation displays error: 'Budget amount is required.'

> [!NOTE]
> **Ghi chú:** Required field validation.

---

### [TC-012] Validation error when entering alphabetic characters in Budget Amount

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.1.3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Input: 'five million'`

**3. Các bước thực hiện (Test Steps):**
1. Enter 'five million' into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Field validation displays error: 'Budget amount must be a valid numeric value.'
2. Form submission is prevented.

> [!NOTE]
> **Ghi chú:** Non-numeric input rejected.

---

### [TC-013] Validation error when entering negative Budget Amount

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: BR6.03` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Input: -50000`

**3. Các bước thực hiện (Test Steps):**
1. Enter -50000 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Field validation displays error: 'Budget amount must be greater than or equal to 0.'
2. Form submission is prevented.

> [!NOTE]
> **Ghi chú:** Negative amount rejected.

---

### [TC-014] Validation error when entering more than 2 decimal places

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: G10` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Input: 125000.456`

**3. Các bước thực hiện (Test Steps):**
1. Enter 125000.456 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Field validation displays error: 'Budget amount can have at most 2 decimal places.'
2. Form submission is prevented.

> [!NOTE]
> **Ghi chú:** Sub-cent precision validation.

---

### [TC-015] Validation error when Budget Amount exceeds proposed cap 999,999,999.99

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-06` |
| **Truy vết (Traceability)** | `FS06: G10` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Input: 1000000000.00`

**3. Các bước thực hiện (Test Steps):**
1. Enter 1000000000.00 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Field validation displays error: 'Budget amount cannot exceed S$ 999,999,999.99.'
2. Form submission is prevented.

> [!NOTE]
> **Ghi chú:** Proposed ceiling validation.

---

### [TC-016] Automatic trimming of whitespace in Budget Amount input

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.1.3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Input: '   3500000   '`

**3. Các bước thực hiện (Test Steps):**
1. Paste '   3500000   ' into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. System trims leading and trailing whitespace.
2. Budget is successfully saved as S$ 3,500,000.00 without error.

> [!NOTE]
> **Ghi chú:** Whitespace sanitization.

---

### [TC-017] Cancel button resets input field to previous configured value

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-005` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `UI` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.1.3, UI-R6-004` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Configured budget is S$ 2,000,000.00.
- 2. MOE HQ user edits amount.

**2. Dữ liệu kiểm thử (Test Data):** `New input: 9999999`

**3. Các bước thực hiện (Test Steps):**
1. Type 9999999 into Budget Amount.
2. Click Cancel button.

**4. Kết quả mong đợi (Expected Result):**
1. Edit is discarded.
2. Field reverts to previous value S$ 2,000,000.00 without making backend changes.

> [!NOTE]
> **Ghi chú:** Cancel button UI verification.

---

## Test Suite: F6.3 SBFAS Budget Setup

### [TC-018] School User views SBFAS Budget page with locked school and scheme labels

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-006` |
| **Test Suite** | `F6.3 SBFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `UI` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.2.3, UI-R6-006, UI-R6-007, BR6.01` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as School Admin (Bukit View Primary).

**2. Dữ liệu kiểm thử (Test Data):** `School: Bukit View Primary School`

**3. Các bước thực hiện (Test Steps):**
1. Open SBFAS Budget Management.
2. Check School and FAS Type elements.

**4. Kết quả mong đợi (Expected Result):**
1. School displays 'Bukit View Primary School' in read-only mode.
2. FAS Type displays 'SBFAS' in read-only mode.
3. Both elements lack editable controls or dropdown selectors.

> [!NOTE]
> **Ghi chú:** Locked scope elements.

---

### [TC-019] Configure SBFAS budget for assigned school with valid amount

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-007` |
| **Test Suite** | `F6.3 SBFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.2.4, AC-R6.1.2, R6-03, R6-04` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as School Admin (Lan Nguyen).
- 2. SBFAS budget form open.

**2. Dữ liệu kiểm thử (Test Data):** `Budget Amount: 150000.00`

**3. Các bước thực hiện (Test Steps):**
1. Enter 150000 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. SBFAS budget is saved for Bukit View Primary School.
2. Confirmation message displays: 'Budget amount has been successfully configured and saved.'
3. Configured Budget Amount displays 'S$ 150,000.00'.

> [!NOTE]
> **Ghi chú:** School budget configuration.

---

### [TC-020] Validation error when SBFAS Budget Amount is negative

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-007` |
| **Test Suite** | `F6.3 SBFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: BR6.03` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as School Admin.

**2. Dữ liệu kiểm thử (Test Data):** `Input: -5000`

**3. Các bước thực hiện (Test Steps):**
1. Enter -5000 into Budget Amount.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Error message displays: 'Budget amount must be greater than or equal to 0.'
2. Save is prevented.

> [!NOTE]
> **Ghi chú:** Negative amount rejected.

---

### [TC-021] Configured budget amount persists across page reload and re-login

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-008` |
| **Test Suite** | `F6.3 SBFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.2.5, R6-04` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. SBFAS budget configured as S$ 150,000.00.

**2. Dữ liệu kiểm thử (Test Data):** `School: BVP-0012`

**3. Các bước thực hiện (Test Steps):**
1. Refresh browser (F5) or sign out and sign in again.
2. Navigate back to SBFAS Budget Management.

**4. Kết quả mong đợi (Expected Result):**
1. Configured Budget Amount persists and displays 'S$ 150,000.00'.
2. Data is not lost upon session refresh.

> [!NOTE]
> **Ghi chú:** Persistence verification.

---

### [TC-022] Save unchanged budget amount does not create redundant state

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-008` |
| **Test Suite** | `F6.3 SBFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.2.4` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Configured budget is S$ 150,000.00.

**2. Dữ liệu kiểm thử (Test Data):** `Budget Amount: 150000.00`

**3. Các bước thực hiện (Test Steps):**
1. Open edit.
2. Keep same amount 150000.00.
3. Click Save.

**4. Kết quả mong đợi (Expected Result):**
1. System handles gracefully.
2. Value remains S$ 150,000.00 without error.

> [!NOTE]
> **Ghi chú:** Idempotent save check.

---

## Test Suite: F6.4 Budget Adjustments

### [TC-023] Edit existing budget opens adjustment modal with current amount

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-009` |
| **Test Suite** | `F6.4 Budget Adjustments` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `UI` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-02` |
| **Truy vết (Traceability)** | `FS06: 5.3.2, UI-R6-015, G2` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Configured budget exists (S$ 150,000.00).
- 2. Edit button is present.

**2. Dữ liệu kiểm thử (Test Data):** `Action: Click Edit`

**3. Các bước thực hiện (Test Steps):**
1. Click Edit button on configured budget view.

**4. Kết quả mong đợi (Expected Result):**
1. Adjustment modal opens.
2. Current allocated amount (S$ 150,000.00) is displayed as reference.
3. New amount input field and Reason field are present.

> [!NOTE]
> **Ghi chú:** Adjustment modal presentation.

---

### [TC-024] Save budget adjustment records adjustment details and reason

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-010` |
| **Test Suite** | `F6.4 Budget Adjustments` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-02` |
| **Truy vết (Traceability)** | `FS06: 5.1.6, G2, G12` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Previous budget: S$ 150,000.00.
- 2. User edits budget.

**2. Dữ liệu kiểm thử (Test Data):** `New Amount: 200000.00, Reason: 'Mid-year FAS allocation top-up'`

**3. Các bước thực hiện (Test Steps):**
1. Enter 200000 into New Amount field.
2. Enter reason.
3. Click Save Adjustment.

**4. Kết quả mong đợi (Expected Result):**
1. Budget updates to S$ 200,000.00.
2. System displays confirmation: 'Budget amount has been successfully configured and saved.'

> [!NOTE]
> **Ghi chú:** Adjustment save flow.

---

### [TC-025] Save button debouncing prevents duplicate submissions on rapid clicks

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-011` |
| **Test Suite** | `F6.4 Budget Adjustments` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Non-functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-12` |
| **Truy vết (Traceability)** | `FS06: Robustness standard` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Budget form filled with valid data.

**2. Dữ liệu kiểm thử (Test Data):** `Rapid double-click on Save button`

**3. Các bước thực hiện (Test Steps):**
1. Rapidly click Save button twice within 250ms.
2. Inspect network tab.

**4. Kết quả mong đợi (Expected Result):**
1. Save button is immediately disabled on first click.
2. Exactly one POST/PUT HTTP request is sent to backend.
3. No duplicate update occurs.

> [!NOTE]
> **Ghi chú:** Debounce mechanism.

---

## Test Suite: F6.5 MOEFAS Statistics

### [TC-026] MOE HQ User views Total Subsidy Amount Granted on MOEFAS Statistics

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-012` |
| **Test Suite** | `F6.5 MOEFAS Statistics` |
| **Giao diện (Page)** | `FAS Subsidy Statistics` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.4.3, UI-R6-018, AC-R6.2.1, R6-05, R6-07` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ (Mei Lin Tan).
- 2. Seeded granted subsidies exist across schools.

**2. Dữ liệu kiểm thử (Test Data):** `Scheme: MOEFAS`

**3. Các bước thực hiện (Test Steps):**
1. Open Subsidy Statistics view.
2. Select MOEFAS scheme view.

**4. Kết quả mong đợi (Expected Result):**
1. Page title displays 'MOEFAS Subsidy Statistics'.
2. FAS Type displays 'MOEFAS'.
3. Total Subsidy Amount Granted displays sum of all granted MOEFAS subsidies formatted as 'S$ #,##0.00'.

> [!NOTE]
> **Ghi chú:** National statistics view.

---

### [TC-027] Statistics aggregation strictly includes only Granted/Approved subsidies

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-013` |
| **Test Suite** | `F6.5 MOEFAS Statistics` |
| **Giao diện (Page)** | `FAS Subsidy Statistics` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.4.5, BR6.04, R6-07` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Seeded applications: Granted (S$ 2,000), Draft (S$ 500), Pending (S$ 800), Rejected (S$ 600).

**2. Dữ liệu kiểm thử (Test Data):** `Applications with diverse statuses`

**3. Các bước thực hiện (Test Steps):**
1. View Total Subsidy Amount Granted on MOEFAS Statistics.
2. Compare total against database sums.

**4. Kết quả mong đợi (Expected Result):**
1. Total Subsidy Amount Granted equals exactly S$ 2,000.00.
2. Amounts from Draft, Pending, and Rejected applications are excluded.

> [!NOTE]
> **Ghi chú:** Status filter integrity.

---

### [TC-028] Empty state displays S$ 0.00 when no grants exist for selected period

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-014` |
| **Test Suite** | `F6.5 MOEFAS Statistics` |
| **Giao diện (Page)** | `FAS Subsidy Statistics` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `UI` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-01` |
| **Truy vết (Traceability)** | `FS06: 5.4.4, Robustness` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.
- 2. Selected period or filter has 0 grants.

**2. Dữ liệu kiểm thử (Test Data):** `Filter: Academic Year 2029 (empty)`

**3. Các bước thực hiện (Test Steps):**
1. Apply filter to period with no grant records.
2. Observe Total Subsidy metric and table.

**4. Kết quả mong đợi (Expected Result):**
1. Total Subsidy Amount Granted displays 'S$ 0.00' (does not show null, NaN, or blank).
2. Table shows empty message: 'No subsidy grant records found for the selected academic year.'

> [!NOTE]
> **Ghi chú:** Empty state handling.

---

## Test Suite: F6.6 SBFAS Statistics

### [TC-029] School User views SBFAS Subsidy Statistics strictly for assigned school

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-015` |
| **Test Suite** | `F6.6 SBFAS Statistics` |
| **Giao diện (Page)** | `FAS Subsidy Statistics` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.5.4, AC-R6.2.2, BR6.01, BR6.02, R6-06` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as School Admin of Bukit View Primary (BVP-0012).
- 2. BVP-0012 has S$ 45,000.00 in granted SBFAS subsidies.
- 3. Meridian Secondary has S$ 90,000.00 in granted SBFAS subsidies.

**2. Dữ liệu kiểm thử (Test Data):** `School: Bukit View Primary School (BVP-0012)`

**3. Các bước thực hiện (Test Steps):**
1. Open SBFAS Subsidy Statistics view.
2. Read Total Subsidy Amount Granted.

**4. Kết quả mong đợi (Expected Result):**
1. Total Subsidy Amount Granted displays exactly 'S$ 45,000.00'.
2. Subsidies belonging to Meridian Secondary are completely excluded.

> [!NOTE]
> **Ghi chú:** School data isolation in stats.

---

### [TC-030] Subsidy Statistics currency adheres to S$ #,##0.00 standard format

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-016` |
| **Test Suite** | `F6.6 SBFAS Statistics` |
| **Giao diện (Page)** | `FAS Subsidy Statistics` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `UI` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.6.2, UI-R6-027, G10` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. SBFAS statistics page open with granted amount S$ 125,000.50.

**2. Dữ liệu kiểm thử (Test Data):** `Amount: 125000.50`

**3. Các bước thực hiện (Test Steps):**
1. Inspect formatted currency string in summary card.

**4. Kết quả mong đợi (Expected Result):**
1. Value displays prefix 'S$ '.
2. Thousands separator comma is used.
3. Exactly two decimal places are rendered: 'S$ 125,000.50'.

> [!NOTE]
> **Ghi chú:** Currency formatting check.

---

### [TC-031] School User views empty state S$ 0.00 when school has zero granted subsidies

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-017` |
| **Test Suite** | `F6.6 SBFAS Statistics` |
| **Giao diện (Page)** | `FAS Subsidy Statistics` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `UI` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.5.4` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as School Admin of school with no granted subsidies.

**2. Dữ liệu kiểm thử (Test Data):** `School: School with 0 grants`

**3. Các bước thực hiện (Test Steps):**
1. Open SBFAS Subsidy Statistics.
2. Inspect summary card and data table.

**4. Kết quả mong đợi (Expected Result):**
1. Total Subsidy Amount Granted displays 'S$ 0.00'.
2. Statistics table displays empty state notification without UI crash.

> [!NOTE]
> **Ghi chú:** Zero grant school stats.

---

## Test Suite: F6.7 Budget Tracking

### [TC-032] Remaining Budget calculation matches formula (Budget - Used)

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-018` |
| **Test Suite** | `F6.7 Budget Tracking` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.9.2, AC-R6.3.3, R6-08, R6-10` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Allocated Budget: S$ 100,000.00.
- 2. Subsidy Amount Used: S$ 35,000.00.

**2. Dữ liệu kiểm thử (Test Data):** `Budget: 100,000, Used: 35,000`

**3. Các bước thực hiện (Test Steps):**
1. Open Budget Tracking view.
2. Observe Allocated Budget, Subsidy Amount Used, and Remaining Budget.

**4. Kết quả mong đợi (Expected Result):**
1. Allocated Budget displays 'S$ 100,000.00'.
2. Subsidy Amount Used displays 'S$ 35,000.00'.
3. Remaining Budget displays 'S$ 65,000.00'.

> [!NOTE]
> **Ghi chú:** Remaining Budget calculation.

---

### [TC-033] Budget Utilization Rate calculation formula verification

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-019` |
| **Test Suite** | `F6.7 Budget Tracking` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.7.3, UI-R6-030, G9` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Allocated Budget: S$ 200,000.00.
- 2. Subsidy Amount Used: S$ 150,000.00.

**2. Dữ liệu kiểm thử (Test Data):** `Budget: 200,000, Used: 150,000`

**3. Các bước thực hiện (Test Steps):**
1. Open Budget Tracking view.
2. Inspect Budget Utilization metric.

**4. Kết quả mong đợi (Expected Result):**
1. Budget Utilization displays '75.0%'.
2. Value matches calculation: (150,000.00 / 200,000.00) * 100% = 75.0%.

> [!NOTE]
> **Ghi chú:** Utilization rate formula check.

---

### [TC-034] Zero division protection when Allocated Budget is 0.00 and Used is 0.00

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-020` |
| **Test Suite** | `F6.7 Budget Tracking` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.7.3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Allocated Budget: S$ 0.00.
- 2. Subsidy Amount Used: S$ 0.00.

**2. Dữ liệu kiểm thử (Test Data):** `Budget: 0.00, Used: 0.00`

**3. Các bước thực hiện (Test Steps):**
1. Open Budget Tracking view.
2. Observe Utilization metric.

**4. Kết quả mong đợi (Expected Result):**
1. Budget Utilization displays '0.0%'.
2. System renders without uncaught DivideByZeroException.

> [!NOTE]
> **Ghi chú:** Zero division robustness.

---

### [TC-035] Real-time sync: Approving application immediately increments Subsidy Used

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-021` |
| **Test Suite** | `F6.7 Budget Tracking` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Integration` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-05` |
| **Truy vết (Traceability)** | `FS06: 5.7.3, G11` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Remaining Budget: S$ 50,000.00, Subsidy Used: S$ 10,000.00.
- 2. SBFAS application approved with S$ 2,500.00 subsidy.

**2. Dữ liệu kiểm thử (Test Data):** `Grant Amount: S$ 2,500.00`

**3. Các bước thực hiện (Test Steps):**
1. Approve SBFAS application in FAS management.
2. Navigate to Budget Tracking view.

**4. Kết quả mong đợi (Expected Result):**
1. Subsidy Amount Used updates to S$ 12,500.00.
2. Remaining Budget updates to S$ 37,500.00.

> [!NOTE]
> **Ghi chú:** Real-time update on grant approval.

---

### [TC-036] Revoking a grant decrements Subsidy Used and restores Remaining Budget

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-021` |
| **Test Suite** | `F6.7 Budget Tracking` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Integration` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-10` |
| **Truy vết (Traceability)** | `FS06: 5.7.5, G7` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Subsidy Used: S$ 12,500.00, Remaining: S$ 37,500.00.
- 2. An approved grant of S$ 2,500.00 is revoked.

**2. Dữ liệu kiểm thử (Test Data):** `Revoked grant: S$ 2,500.00`

**3. Các bước thực hiện (Test Steps):**
1. Revoke the FAS grant.
2. Open Budget Tracking view.

**4. Kết quả mong đợi (Expected Result):**
1. Subsidy Amount Used decrements to S$ 10,000.00.
2. Remaining Budget increments to S$ 50,000.00.

> [!NOTE]
> **Ghi chú:** Grant revocation rollback.

---

### [TC-037] Remaining Budget precision with fractional cent rounding

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-020` |
| **Test Suite** | `F6.7 Budget Tracking` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: G10` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Budget: S$ 10,000.00.
- 2. Grant 1: S$ 333.33, Grant 2: S$ 666.67 (Total Used: S$ 1,000.00).

**2. Dữ liệu kiểm thử (Test Data):** `Grants: 333.33 and 666.67`

**3. Các bước thực hiện (Test Steps):**
1. View Remaining Budget on dashboard.

**4. Kết quả mong đợi (Expected Result):**
1. Remaining Budget displays exactly S$ 9,000.00 without floating point drift.

> [!NOTE]
> **Ghi chú:** Fractional cents integrity.

---

## Test Suite: F6.8 Budget Warnings

### [TC-038] Normal state displayed when budget utilization is below 80%

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-022` |
| **Test Suite** | `F6.8 Budget Warnings` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `UI` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-03` |
| **Truy vết (Traceability)** | `FS06: 5.7.3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Budget: S$ 100,000.00, Used: S$ 50,000.00 (50.0% utilization).

**2. Dữ liệu kiểm thử (Test Data):** `Utilization: 50.0%`

**3. Các bước thực hiện (Test Steps):**
1. Open Budget Tracking view.
2. Check status indicator.

**4. Kết quả mong đợi (Expected Result):**
1. Utilization displays '50.0%'.
2. Indicator displays normal status.
3. No warning alert banner is displayed.

> [!NOTE]
> **Ghi chú:** Normal utilization indicator.

---

### [TC-039] Warning Banner displayed when budget utilization reaches 80.0% threshold

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-022` |
| **Test Suite** | `F6.8 Budget Warnings` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-03` |
| **Truy vết (Traceability)** | `FS06: R6-11, BR6.06` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Budget: S$ 100,000.00, Used: S$ 80,000.00 (80.0% utilization).

**2. Dữ liệu kiểm thử (Test Data):** `Utilization: 80.0%`

**3. Các bước thực hiện (Test Steps):**
1. Open Budget Tracking view.

**4. Kết quả mong đợi (Expected Result):**
1. System displays warning banner: 'Warning: SBFAS budget utilization has reached 80.0%. Remaining balance: S$ 20,000.00.'

> [!NOTE]
> **Ghi chú:** 80% warning threshold.

---

### [TC-040] Warning Banner not displayed when budget utilization is 79.9%

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-022` |
| **Test Suite** | `F6.8 Budget Warnings` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-03` |
| **Truy vết (Traceability)** | `FS06: R6-11, BR6.06` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Budget: S$ 100,000.00, Used: S$ 79,900.00 (79.9% utilization).

**2. Dữ liệu kiểm thử (Test Data):** `Utilization: 79.9%`

**3. Các bước thực hiện (Test Steps):**
1. Open Budget Tracking view.

**4. Kết quả mong đợi (Expected Result):**
1. System does not display warning banner.
2. Utilization indicator remains in normal state.

> [!NOTE]
> **Ghi chú:** 79.9% boundary test.

---

### [TC-041] Alert Banner displayed when budget is fully exhausted (Remaining = S$ 0.00)

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-023` |
| **Test Suite** | `F6.8 Budget Warnings` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-04` |
| **Truy vết (Traceability)** | `FS06: R6-11, BR6.06, G3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Budget: S$ 100,000.00, Used: S$ 100,000.00 (100.0% utilization).

**2. Dữ liệu kiểm thử (Test Data):** `Utilization: 100.0%, Remaining: S$ 0.00`

**3. Các bước thực hiện (Test Steps):**
1. Open Budget Tracking view.

**4. Kết quả mong đợi (Expected Result):**
1. System displays alert banner: 'Alert: The budget allocation for this scheme has been exhausted.'
2. Remaining Budget displays S$ 0.00.

> [!NOTE]
> **Ghi chú:** 100% exhaustion alert.

---

### [TC-042] Budget Deficit displayed when Subsidy Used exceeds Allocated Budget

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-024` |
| **Test Suite** | `F6.8 Budget Warnings` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-04` |
| **Truy vết (Traceability)** | `FS06: 5.9.2, G3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Budget: S$ 100,000.00, Used: S$ 115,000.00 (115.0% utilization).

**2. Dữ liệu kiểm thử (Test Data):** `Remaining: -S$ 15,000.00`

**3. Các bước thực hiện (Test Steps):**
1. Open Budget Tracking view.

**4. Kết quả mong đợi (Expected Result):**
1. Remaining Budget displays '-S$ 15,000.00'.
2. Deficit indicator is displayed.
3. Utilization displays '115.0%'.

> [!NOTE]
> **Ghi chú:** Budget deficit negative currency.

---

## Test Suite: F6.9 Non-blocking Grant

### [TC-043] School Admin successfully approves SBFAS application when budget is exhausted

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-025` |
| **Test Suite** | `F6.9 Non-blocking Grant` |
| **Giao diện (Page)** | `FAS Application Review` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: BR6.06, R6-11, G3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. School SBFAS Remaining Budget is S$ 0.00.
- 2. Pending SBFAS application exists for student Alex Tan.

**2. Dữ liệu kiểm thử (Test Data):** `Application: APP-SBFAS-2026-091`

**3. Các bước thực hiện (Test Steps):**
1. Open pending SBFAS application.
2. Click Approve SBFAS button.
3. Confirm action.

**4. Kết quả mong đợi (Expected Result):**
1. Application is successfully approved (Status: Approved SBFAS).
2. Action is NOT blocked by zero budget.
3. Grant is committed, and Remaining Budget becomes negative (-S$ 800.00).

> [!NOTE]
> **Ghi chú:** CORE POLICY: Non-blocking SBFAS grant.

---

### [TC-044] MOE Officer manual MOEFAS approval blocked due to contradiction with FS04

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-026` |
| **Test Suite** | `F6.9 Non-blocking Grant` |
| **Giao diện (Page)** | `FAS Application Review` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Block`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-07` |
| **Truy vết (Traceability)** | `FS04 vs FS06: BR6.06, G4` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. National MOEFAS Remaining Budget is S$ 0.00.
- 2. Form closed.

**2. Dữ liệu kiểm thử (Test Data):** `Application: APP-MOEFAS-2026-140`

**3. Các bước thực hiện (Test Steps):**
1. Attempt to find manual 'Approve MOEFAS' button in MOE HQ review drawer.

**4. Kết quả mong đợi (Expected Result):**
1. In FS04, MOE HQ has no Approve button (MOEFAS is auto-assessed by system).
2. Case is BLOCKED pending BA clarification on MOEFAS grant mechanism.

> [!NOTE]
> **Ghi chú:** Contradiction with FS04 (MOE HQ does not manually approve MOEFAS).

---

### [TC-045] Advisory notice displayed upon approving over-budget application without disabling submit

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-027` |
| **Test Suite** | `F6.9 Non-blocking Grant` |
| **Giao diện (Page)** | `FAS Application Review` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `UI` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-03` |
| **Truy vết (Traceability)** | `FS06: BR6.06, R6-11` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Remaining Budget is S$ 0.00.
- 2. Approver clicks Approve SBFAS.

**2. Dữ liệu kiểm thử (Test Data):** `Action: Approve SBFAS`

**3. Các bước thực hiện (Test Steps):**
1. Observe confirmation modal text and buttons.

**4. Kết quả mong đợi (Expected Result):**
1. Modal displays advisory notice: 'Budget Limit Notice: Current budget balance is insufficient, but granting is permitted under policy rules. Proceed?'
2. 'Confirm' button is active and enabled.

> [!NOTE]
> **Ghi chú:** Advisory deficit notice.

---

## Test Suite: F6.10 Edge Cases & Security

### [TC-046] Boundary test: Minimum positive budget amount S$ 0.01

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-028` |
| **Test Suite** | `F6.10 Edge Cases & Security` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: BR6.03` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as School Admin.

**2. Dữ liệu kiểm thử (Test Data):** `Input: 0.01`

**3. Các bước thực hiện (Test Steps):**
1. Enter 0.01 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Value 0.01 is accepted and saved.
2. Configured Budget Amount displays 'S$ 0.01'.

> [!NOTE]
> **Ghi chú:** Minimum positive currency bound.

---

### [TC-047] Boundary test: Maximum allowable budget amount S$ 999,999,999.99

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-028` |
| **Test Suite** | `F6.10 Edge Cases & Security` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-06` |
| **Truy vết (Traceability)** | `FS06: G10` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Input: 999999999.99`

**3. Các bước thực hiện (Test Steps):**
1. Enter 999999999.99 into Budget Amount.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Value is saved successfully.
2. Configured Budget Amount displays 'S$ 999,999,999.99'.

> [!NOTE]
> **Ghi chú:** Proposed upper bound check.

---

### [TC-048] Optimistic concurrency conflict detection when two admins edit same budget

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-029` |
| **Test Suite** | `F6.10 Edge Cases & Security` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Integration` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-11` |
| **Truy vết (Traceability)** | `FS06: Robustness standard` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-02 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Admin A and Admin B open the same budget record (S$ 150,000.00).
- 2. Admin A updates amount to S$ 160,000.00 and saves successfully.

**2. Dữ liệu kiểm thử (Test Data):** `Admin B attempts to save S$ 170,000.00 with stale version`

**3. Các bước thực hiện (Test Steps):**
1. Admin B clicks Save button.

**4. Kết quả mong đợi (Expected Result):**
1. System detects concurrency conflict.
2. Error displays: 'The budget record has been modified by another user. Please refresh and try again.'
3. Admin A changes are not overwritten.

> [!NOTE]
> **Ghi chú:** Optimistic concurrency control.

---

### [TC-049] XSS payload in Reason field is escaped and rendered safely

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-030` |
| **Test Suite** | `F6.10 Edge Cases & Security` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Security` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-02` |
| **Truy vết (Traceability)** | `FS06: Security standard` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Adjustment modal open.

**2. Dữ liệu kiểm thử (Test Data):** `Reason: <script>alert(1)</script>`

**3. Các bước thực hiện (Test Steps):**
1. Paste script tag into Reason field.
2. Save and view audit log/reason.

**4. Kết quả mong đợi (Expected Result):**
1. Input is safely HTML-escaped.
2. No script execution occurs in browser.

> [!NOTE]
> **Ghi chú:** XSS protection in reason field.

---

### [TC-050] Backend API validates non-negative amount when client validation bypassed

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-030` |
| **Test Suite** | `F6.10 Edge Cases & Security` |
| **Giao diện (Page)** | `API Gateway` |
| **Độ nghiêm trọng (Severity)** | `S1 (highest)` |
| **Độ ưu tiên (Priority)** | `Critical` |
| **Loại kiểm thử (Test Type)** | `Security` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: BR6.03` |
| **Môi trường (Environment)** | API Gateway: http://localhost:5273 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Intercepting API call directly with valid authorization token.

**2. Dữ liệu kiểm thử (Test Data):** `Payload: {"schoolId": "BVP-0012", "allocatedBudgetAmount": -50000.00}`

**3. Các bước thực hiện (Test Steps):**
1. Send POST request with negative amount directly to backend API.

**4. Kết quả mong đợi (Expected Result):**
1. Backend rejects request with HTTP 400 Bad Request.
2. Error details: 'Budget amount must be greater than or equal to 0.'
3. Database is not updated.

> [!NOTE]
> **Ghi chú:** Zero-trust backend validation.

---

## Test Suite: F6.2 MOEFAS Budget Setup

### [TC-051] Budget amount rejects scientific exponential notation e.g. 1e6

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.1.3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Input: 1e6`

**3. Các bước thực hiện (Test Steps):**
1. Type 1e6 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Field validation displays error: 'Budget amount must be a valid numeric value.'
2. Exponential format is rejected.

> [!NOTE]
> **Ghi chú:** Exponential notation rejected.

---

### [TC-052] Budget amount rejects raw currency symbol input e.g. $50000

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-004` |
| **Test Suite** | `F6.2 MOEFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S3` |
| **Độ ưu tiên (Priority)** | `Medium` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.1.3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.

**2. Dữ liệu kiểm thử (Test Data):** `Input: $50000`

**3. Các bước thực hiện (Test Steps):**
1. Paste $50000 into Budget Amount field.
2. Click Save button.

**4. Kết quả mong đợi (Expected Result):**
1. Field validation displays error: 'Budget amount must be a valid numeric value.'
2. Currency symbols in raw input are rejected.

> [!NOTE]
> **Ghi chú:** Currency symbol rejected in raw input.

---

## Test Suite: F6.3 SBFAS Budget Setup

### [TC-053] Initial budget setup for newly onboarded school with zero grant history

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-007` |
| **Test Suite** | `F6.3 SBFAS Budget Setup` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Draft`** |
| **Giả định tham chiếu (Assumption Ref)** | `ASM-R6-09` |
| **Truy vết (Traceability)** | `FS06: 5.2.4, 5.8.3, R6-04` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as School Admin of newly onboarded school.

**2. Dữ liệu kiểm thử (Test Data):** `Budget: S$ 80,000.00`

**3. Các bước thực hiện (Test Steps):**
1. Configure initial budget of S$ 80,000.00.
2. Open tracking view.

**4. Kết quả mong đợi (Expected Result):**
1. Allocated: S$ 80,000.00, Used: S$ 0.00, Remaining: S$ 80,000.00, Utilization: 0.0%.

> [!NOTE]
> **Ghi chú:** New school initial onboarding.

---

## Test Suite: F6.5 MOEFAS Statistics

### [TC-054] Subsidy Statistics accurately handles multiple grants per student

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-013` |
| **Test Suite** | `F6.5 MOEFAS Statistics` |
| **Giao diện (Page)** | `FAS Subsidy Statistics` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.6.1, BR6.04` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Student has 2 granted subsidies: Textbook ($300) and Uniform ($150).

**2. Dữ liệu kiểm thử (Test Data):** `Student: STU-BVP-01`

**3. Các bước thực hiện (Test Steps):**
1. View Subsidy Statistics dashboard.

**4. Kết quả mong đợi (Expected Result):**
1. Both subsidies ($450 total) are correctly summed into Total Subsidy Amount Granted.

> [!NOTE]
> **Ghi chú:** Multi-grant aggregation per student.

---

## Test Suite: F6.1 Access & Authorization

### [TC-055] Viewing budget when not yet configured shows unconfigured state

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-001` |
| **Test Suite** | `F6.1 Access & Authorization` |
| **Giao diện (Page)** | `FAS Budget Management` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.3.1, R6.1.3` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. School has no budget configured yet in database.

**2. Dữ liệu kiểm thử (Test Data):** `School: Unconfigured School`

**3. Các bước thực hiện (Test Steps):**
1. Open budget view as school user.

**4. Kết quả mong đợi (Expected Result):**
1. System displays prompt: 'No budget configured yet for this scheme.'
2. 'Configure Budget' button is available.

> [!NOTE]
> **Ghi chú:** Unconfigured budget view.

---

## Test Suite: F6.7 Budget Tracking

### [TC-056] Separate budget tracking view for MOEFAS national scheme

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Scenario ID** | `TS-018` |
| **Test Suite** | `F6.7 Budget Tracking` |
| **Giao diện (Page)** | `FAS Budget Tracking` |
| **Độ nghiêm trọng (Severity)** | `S2` |
| **Độ ưu tiên (Priority)** | `High` |
| **Loại kiểm thử (Test Type)** | `Functional` |
| **Trạng thái Review (Review Status)** | **`Approve`** |
| **Giả định tham chiếu (Assumption Ref)** | `N/A` |
| **Truy vết (Traceability)** | `FS06: 5.7.1, R6.3.1` |
| **Môi trường (Environment)** | Admin Portal: http://localhost:5173 Needs: ENV-R6-01, ENV-R6-03 |

**1. Điều kiện tiên quyết (Preconditions):**
- 1. Signed in as MOE HQ.
- 2. National MOEFAS budget configured.

**2. Dữ liệu kiểm thử (Test Data):** `Scheme: MOEFAS`

**3. Các bước thực hiện (Test Steps):**
1. Open MOEFAS Budget Tracking view.

**4. Kết quả mong đợi (Expected Result):**
1. View displays national MOEFAS Budget Amount, national Subsidy Amount Used, and Remaining Budget.
2. Values reflect nationwide aggregation.

> [!NOTE]
> **Ghi chú:** Dedicated MOEFAS tracking.

---

