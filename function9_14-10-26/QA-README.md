# Function 9 — Billing & Payment: hướng dẫn setup local cho QA

Tài liệu này hướng dẫn QA chạy và kiểm thử flow Billing & Payment bằng source code trong package. Tất cả lệnh bên dưới được chạy từ **thư mục gốc sau khi giải nén package** — thư mục chứa `EduGovernment-FrontEnd` và `EduGovernment-Backend`.

## 1. Phạm vi và giới hạn hiện tại

Flow cần kiểm thử:

1. Parent mở **Fees & Payments**.
2. Xem outstanding fees của demo student.
3. Chọn một hoặc nhiều `student_charge`.
4. Chọn phương thức Education Account, Online Payment hoặc Both.
5. Review và bấm **Authorize & Pay**.
6. Với Online/Both, thanh toán qua payment simulator.
7. E-service poll transaction và hiển thị receipt từ Billing API.

Giới hạn của môi trường hiện tại:

- Child context là DEV fixture, chưa có API parent-to-children từ F1/F3.
- Demo student cố định:
  `11111111-1111-1111-1111-111111111111`.
- Demo wallet cố định:
  `33333333-3333-3333-3333-333333333333`.
- Education Account balance là stub, mặc định SGD 250.00.
- Outstanding fees hiện do Billing BE fixture cung cấp, không nằm trong bảng `student_charges` của Billing DB.
- EA deduction được ghi nhận trong Billing DB và log `[STUB] EducationAccountService deduct`; không kỳ vọng database EducationAccountService bị trừ tiền.
- Both failure có thể thành `ReconciliationRequired`; BE hiện tại chưa tự reverse EA leg.
- Payment failure vẫn materialize invoice/items. Không có retry API cho cùng các charges đã materialize.

## 2. Yêu cầu cài đặt

Cài trên máy QA:

- Docker Desktop đang chạy.
- .NET SDK phù hợp với solution trong `EduGovernment-Backend`.
- Node.js >= 22.12 và npm >= 10.
- PowerShell 5.1 hoặc PowerShell 7.
- Trình duyệt Chrome/Edge.

Không cần cài `node_modules` sẵn. Frontend sẽ cài bằng `npm ci`.

## 3. Port sử dụng

| Thành phần | URL |
|---|---|
| SQL Server container | `localhost:1433` |
| Billing API | `http://localhost:5008` |
| Payment Simulator API | `http://localhost:5286` |
| Payment Simulator FE | `http://localhost:5176` |
| E-service FE | `http://localhost:5174` |

Nếu một port đã được process khác sử dụng, dừng process đó trước khi chạy test.

## 4. Khởi động SQL Server bằng Docker

Mở Terminal 1 tại root package:

```powershell
Set-Location .\EduGovernment-Backend

docker compose -f ".\deploy\docker\docker-compose.infra.yml" up -d sqlserver
docker compose ps
```

Chờ tới khi `sqlserver` ở trạng thái `healthy`.

Compose này chỉ khởi động SQL Server cho Function 9. Không chạy toàn bộ stack microservices bằng profile `all`.

Nếu máy chưa cài .NET 10 thì chạy 2 bước sau:
1. Mở PowerShell Run as Administrator rồi chạy:

```powershell
winget install --id Microsoft.DotNet.SDK.10 --exact --source winget
```

2. Cài xong mở PowerShell mới và kiểm tra:

```powershell
dotnet --list-sdks
```

hiện thông tin .NET 10 là ổn

## Lưu ý trước khi khởi động các phần BE bên dưới: DOCKER + .NET 10 PHẢI TẢI VỀ THÀNH CÔNG thì mới khởi động BE được

## 5. Khởi động Billing API

Mở Terminal 2 tại root package:

```powershell
Set-Location .\EduGovernment-Backend

$env:Database__ConnectionString = "Server=localhost,1433;Database=BillingPaymentService;User Id=sa;Password=YourStrong@Password123;TrustServerCertificate=True;MultipleActiveResultSets=True;"
$env:Database__AutoMigrate = "true"

dotnet run `
  --project .\BillingPaymentService\API\BillingPaymentService.API.csproj `
  --launch-profile http
```

Kiểm tra Billing API:

```powershell
Invoke-WebRequest http://localhost:5008/health
```

Kỳ vọng HTTP `200`.

## 6. Khởi động Payment Simulator API

Mở Terminal 3 tại root package:

```powershell
Set-Location .\EduGovernment-Backend

dotnet run `
  --project .\Simulation\OnlinePaymentGatewaySimulation\OnlinePaymentGatewaySimulation.csproj `
  --launch-profile http
```

Kiểm tra simulator:

```powershell
Invoke-WebRequest http://localhost:5286/health
```

Kỳ vọng HTTP `200`.

## 7. Cài và chạy frontend

Mở Terminal 4 tại root package:

```powershell
Set-Location .\EduGovernment-FrontEnd

npm ci
npm run dev:payment-checkout
```

Payment Simulator FE chạy tại `http://localhost:5176`.

Mở Terminal 5 tại root package:

```powershell
Set-Location .\EduGovernment-FrontEnd

npm run dev:eservice
```

E-service chạy tại `http://localhost:5174`.

Mở trình duyệt tại:

```text
http://localhost:5174
```

Trong môi trường DEV, chọn navigation **Fees & Payments**. 
Nếu refresh trực tiếp, route demo vẫn dùng được:

```text
http://localhost:5174/billing/11111111-1111-1111-1111-111111111111
```

Frontend proxy `/api/billing` tới Billing API `localhost:5008`. Browser phải gọi được các endpoint sau:

```text
GET  /api/billing/v1/students/{studentId}/outstanding-charges
POST /api/billing/v1/checkout
GET  /api/billing/v1/transactions/{transactionId}
GET  /api/billing/v1/invoices/{invoiceId}
```

## 8. Kiểm tra dữ liệu ban đầu

Mở PowerShell tại bất kỳ thư mục nào:

```powershell
$studentId = "11111111-1111-1111-1111-111111111111"

Invoke-RestMethod `
  "http://localhost:5008/api/v1/students/$studentId/outstanding-charges"
```

Kỳ vọng có 3 charges:

| Student charge | Net amount |
|---|---:|
| `aaaa0001-0000-0000-0000-000000000001` | SGD 210.00 |
| `aaaa0001-0000-0000-0000-000000000002` | SGD 140.00 |
| `aaaa0002-0000-0000-0000-000000000001` | SGD 120.00 |
| **Total** | **SGD 470.00** |

## 9. Reset demo data trước mỗi scenario

Checkout sẽ materialize invoice và làm charge biến mất khỏi outstanding list. Vì vậy cần reset trước mỗi scenario.

Chạy từ root package:

```powershell
$sql = @"
USE [BillingPaymentService];

SET ANSI_NULLS ON;
SET ANSI_PADDING ON;
SET ANSI_WARNINGS ON;
SET ARITHABORT ON;
SET CONCAT_NULL_YIELDS_NULL ON;
SET QUOTED_IDENTIFIER ON;
SET NUMERIC_ROUNDABORT OFF;
SET XACT_ABORT ON;

DECLARE @StudentId UNIQUEIDENTIFIER = '11111111-1111-1111-1111-111111111111';
DECLARE @ids TABLE (Id VARCHAR(50));

INSERT INTO @ids
SELECT Id
FROM dbo.invoices
WHERE StudentId = @StudentId;

BEGIN TRY
  BEGIN TRANSACTION;

  DELETE FROM dbo.payment_webhook_receipts
  WHERE FundingTransactionId IN (
    SELECT Id
    FROM dbo.transaction_funding_sources
    WHERE TransactionId IN (
      SELECT Id FROM dbo.transactions
      WHERE InvoiceId IN (SELECT Id FROM @ids)
    )
  );

  DELETE FROM dbo.transaction_funding_sources
  WHERE TransactionId IN (
    SELECT Id FROM dbo.transactions
    WHERE InvoiceId IN (SELECT Id FROM @ids)
  );

  DELETE FROM dbo.transactions
  WHERE InvoiceId IN (SELECT Id FROM @ids);

  DELETE FROM dbo.invoice_items
  WHERE InvoiceId IN (SELECT Id FROM @ids);

  DELETE FROM dbo.invoices
  WHERE Id IN (SELECT Id FROM @ids);

  COMMIT TRANSACTION;
END TRY
BEGIN CATCH
  IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
  THROW;
END CATCH;
"@

docker exec template-sqlserver `
  /opt/mssql-tools18/bin/sqlcmd `
  -S localhost `
  -U sa `
  -P 'YourStrong@Password123' `
  -C `
  -Q $sql
```

Nếu container có tên khác, xem tên bằng:

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}"
```

Không dùng `docker compose down -v` khi chỉ muốn reset scenario, vì lệnh đó xóa database volume.

## 10. Manual test scenarios

### Scenario A — Load và selection

1. Mở **Fees & Payments**.
2. Kiểm tra 3 charges và total SGD 470.00.
3. Kiểm tra EA balance SGD 250.00.
4. Chọn một charge.
5. Chọn nhiều charge.
6. Dùng **Select all outstanding fees**.
7. Bỏ chọn từng charge.
8. Kiểm tra tổng selected amount.
9. Bấm Continue.

Expected:

- Continue bị disabled khi chưa chọn fee.
- Continue chỉ đổi UI step, không tạo invoice/transaction.
- Network trước Authorize chỉ có GET outstanding charges.

### Scenario B — Education Account success

1. Reset demo data.
2. Chọn charge SGD 120 hoặc SGD 210.
3. Giữ Education Account mặc định.
4. Đi qua Payment method và Review.
5. Bấm **Authorize & Pay**.

Expected:

- Không mở simulator.
- Result chuyển thành `Succeeded`.
- Receipt hiển thị invoice, transaction và EA funding breakdown.
- DB có invoice `Paid`, transaction `Succeeded`, một EA funding leg `Succeeded`.
- Không có webhook receipt.

### Scenario C — Online success

1. Reset demo data.
2. Chọn charge SGD 120.
3. Chọn Online Payment.
4. Bấm Authorize.
5. Simulator mở ở `http://localhost:5176`.
6. Chọn **Pay successful**.
7. Kiểm tra browser quay về `http://localhost:5174/payment-result`.

Expected:

- Trước outcome: transaction và online leg `Pending`.
- Sau outcome: invoice `Paid`, transaction `Succeeded`, online leg `Succeeded`.
- Có webhook receipt `Processed`.
- Result page dừng polling sau terminal status.

### Scenario D — Both success

1. Reset demo data.
2. Chọn charge SGD 210 + SGD 140 = SGD 350.
3. Kiểm tra Education Account bị disabled.
4. Kiểm tra Both là phương thức mặc định.
5. Kiểm tra split read-only: EA SGD 250 + Online SGD 100.
6. Authorize và chọn **Pay successful** trên simulator.

Expected:

- Một invoice có hai invoice items.
- Hai funding legs: EA SGD 250 và Online SGD 100.
- Transaction `Succeeded`, invoice `Paid`.
- Webhook receipt `Processed` cho online leg.

### Scenario E — Online failure

1. Reset demo data.
2. Chọn Online Payment.
3. Trên simulator chọn **Pay failed**.

Expected:

- UI hiển thị `Failed`.
- Không hiển thị cam kết retry cùng charges.
- Invoice vẫn tồn tại ở `PaymentPending`.
- Transaction và online leg `Failed`.
- Webhook receipt `Processed`.

### Scenario F — Both failure / reconciliation

1. Reset demo data.
2. Chọn SGD 210 + SGD 140.
3. Chọn Both.
4. Trên simulator chọn **Pay failed**.

Expected:

- UI hiển thị `ReconciliationRequired`.
- Không hiển thị “EA đã được hoàn” nếu EA leg vẫn `Succeeded`.
- Hiển thị cảnh báo EA portion có thể đã bị trừ và cần reconciliation/support.
- DB: transaction `ReconciliationRequired`, EA leg `Succeeded`, Online leg `Failed`.
- `EducationAccountReversalTransactionId` vẫn null.
- Billing log có thông tin TODO reverse EA leg.

### Scenario G — Stale charge / conflict

1. Reset demo data.
2. Mở cùng một student ở hai tab.
3. Tab 1 thanh toán một charge.
4. Tab 2 dùng danh sách cũ và cố thanh toán cùng charge.

Expected:

- Tab 2 nhận lỗi stale/409.
- Selection bị xóa.
- Trang quay về selection và refetch charges.
- Không tạo invoice item thứ hai cho cùng `StudentChargeId`.

## 11. Kiểm tra Browser DevTools

Trong Network:

- Outstanding request là `GET /api/billing/v1/...`.
- Chỉ nút **Authorize & Pay** mới tạo `POST /api/billing/v1/checkout`.
- Checkout có header `Idempotency-Key`.
- Không có header `X-User-Id`.
- EA payload có `walletId`, không có `returnUrl`.
- Online payload có `returnUrl`, không có `walletId`.
- Both payload có cả `walletId` và `returnUrl`.
- Transaction polling lặp khoảng 2 giây khi status `Pending`.
- Polling dừng khi status terminal.

Trong Console:

- Không có exception JavaScript.
- Có thể bỏ qua warning không ảnh hưởng tới flow nếu không có request thất bại.

Kiểm tra responsive tại:

```text
320px, 768px, 1024px, 1440px
```

Kiểm tra thêm keyboard navigation cho checkbox, radio, Back và Authorize.

## 12. Kiểm tra Billing DB

Chạy query sau trong SQL client hoặc qua `sqlcmd`:

```sql
USE [BillingPaymentService];

DECLARE @StudentId UNIQUEIDENTIFIER =
  '11111111-1111-1111-1111-111111111111';

DECLARE @InvoiceId VARCHAR(50) = (
  SELECT TOP 1 Id
  FROM dbo.invoices
  WHERE StudentId = @StudentId
  ORDER BY CreatedAt DESC
);

SELECT *
FROM dbo.invoices
WHERE Id = @InvoiceId;

SELECT *
FROM dbo.invoice_items
WHERE InvoiceId = @InvoiceId
ORDER BY LineNumber;

SELECT *
FROM dbo.transactions
WHERE InvoiceId = @InvoiceId
ORDER BY CreatedAt DESC;

SELECT fs.*
FROM dbo.transaction_funding_sources fs
JOIN dbo.transactions tx ON tx.Id = fs.TransactionId
WHERE tx.InvoiceId = @InvoiceId
ORDER BY fs.SequenceNumber;

SELECT wr.*
FROM dbo.payment_webhook_receipts wr
JOIN dbo.transaction_funding_sources fs
  ON fs.Id = wr.FundingTransactionId
JOIN dbo.transactions tx ON tx.Id = fs.TransactionId
WHERE tx.InvoiceId = @InvoiceId
ORDER BY wr.ReceivedAt;
```

Status thường gặp:

```text
Invoice:    3 = PaymentPending, 4 = Paid
Transaction: 1 = Pending, 2 = Succeeded, 3 = Failed, 5 = ReconciliationRequired
Funding:    1 = Pending, 2 = Succeeded, 3 = Failed, 4 = Reversed
Webhook:    2 = Processed
```

## 13. Kiểm tra log

Nếu chạy API trực tiếp bằng `dotnet run`, giữ nguyên terminal để xem log.

Các log cần lưu:

- POST checkout và payload đã nhận.
- Balance lookup.
- `[STUB] EducationAccountService deduct` cho EA leg.
- Online webhook outcome.
- TODO reverse EA leg trong Both failure.
- Transaction status transition.

Nếu chạy bằng script có redirect log, xem:

```powershell
Get-Content "$env:TEMP\function9-test-logs\billing.out.log" -Wait
Get-Content "$env:TEMP\function9-test-logs\sim.out.log" -Wait
```

Các warning EF liên quan MARS hoặc multiple collection include không được xem là lỗi nếu request vẫn trả HTTP thành công và DB state đúng.

## 14. Automated verification tùy chọn

Chạy từ `EduGovernment-FrontEnd`:

```powershell
Set-Location .\EduGovernment-FrontEnd

npm run test -w e-service
npm run test -w payment-checkout-simulator
npm run test -w @edusave/i18n

npm run typecheck -w e-service
npm run typecheck -w payment-checkout-simulator
npm run typecheck -w @edusave/i18n

npm run lint -w e-service
npm run lint -w payment-checkout-simulator
npm run lint -w @edusave/i18n

npm run build:eservice
npm run build:payment-checkout
```

Từ `EduGovernment-Backend`:

```powershell
Set-Location .\EduGovernment-Backend
dotnet test .\BillingPaymentService\Tests\BillingPaymentService.UnitTests\BillingPaymentService.UnitTests.csproj
```

## 15. Bằng chứng QA cần lưu

Cho mỗi scenario, lưu:

- screenshot các màn selection, method, review và result;
- Browser Network request/response;
- transaction ID và invoice ID;
- kết quả query DB;
- log Billing API và simulator;
- viewport và locale đã dùng;
- thời điểm reset dữ liệu.

## 16. Dừng môi trường

Dừng frontend/API bằng `Ctrl+C` ở từng terminal.

Dừng SQL Server nhưng giữ lại volume:

```powershell
Set-Location .\EduGovernment-Backend
docker compose stop sqlserver
```

Chỉ xóa database volume khi thực sự muốn làm sạch toàn bộ local environment:

```powershell
docker compose down -v
```

Lệnh cuối sẽ xóa dữ liệu Billing DB trong Docker volume.
