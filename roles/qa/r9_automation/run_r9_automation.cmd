@echo off
rem Chay bo automation FS09 (Fees & Payments) tren Chrome cua may. Khong chay trong Claude.
rem   run_r9_automation.cmd                 smoke (mac dinh, gom ca trang dang nhap admin portal), chi doc, an toan
rem   run_r9_automation.cmd read            moi test chi doc, gia lap va API bi tu choi (khong ghi du lieu)
rem   run_r9_automation.cmd pay             them test THANH TOAN THAT (tieu khoan phi, tru tien vi). Phai go PAY de xac nhan
rem   run_r9_automation.cmd destructive     test rut can vi cua mot con (chia khoan Both). Phai go DRAIN de xac nhan
rem   run_r9_automation.cmd full            CHAY HET moi test, ke ca ghi du lieu that (pay) va rut can vi (destructive), KHONG hoi xac nhan
rem   run_r9_automation.cmd rules           34 case quy tac kiem tra du lieu moi (TC-173 den TC-206), file tests\test_f99_validation_rules.py
rem   run_r9_automation.cmd suite 3         mot nhom, F9.3 o day (1 den 5, hoac 7)
rem   run_r9_automation.cmd tc 046          mot case, TC-046 o day
rem   run_r9_automation.cmd draft           case phu thuoc gia dinh chua duoc BA xac nhan
rem   run_r9_automation.cmd defects         case ky vong that bai vi ban build lech voi R9
rem   run_r9_automation.cmd allure          mo bao cao Allure da co (artifacts\allure-report), tao lai tu allure-results neu chua co
rem   them chu headed o cuoi de xem trinh duyet, vi du: run_r9_automation.cmd suite 3 headed
rem CHI CHAY TREN LOCALHOST: dia chi chua vercel.app hoac may khac localhost bi chan ngay (data\seed.py, conftest.py). Khong chay tren Vercel.
rem Hai dia chi: e-service R9_BASE_URL (mac dinh http://localhost:5174), admin portal R9_ADMIN_URL (mac dinh http://localhost:5173)
rem Bien moi truong tuy chon: R9_BASE_URL, R9_ADMIN_URL, R9_NRIC, R9_CHECKOUT_URL, R9_EXPECTED_CHILDREN (xem README.md)
setlocal EnableExtensions
cd /d "%~dp0"
for %%V in (R9_BASE_URL R9_ADMIN_URL R9_CHECKOUT_URL) do call :checkurl %%V || exit /b 2
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
rem Khong dat R9_EXPECTED_CHILDREN: TC-006 tu lay danh sach con cua persona tu DB (cot father_nric / mother_nric), nen dung ca khi nap them seed R9.

set "MODE=%~1"
if "%MODE%"=="" set "MODE=smoke"
set "ARG=%~2"
set "HEADED="
for %%A in (%*) do if /i "%%~A"=="headed" set "HEADED=--headed --slowmo 150"
for %%A in (%*) do if /i "%%~A"=="each" set "R9_RESEED_EACH=1"

if /i "%MODE%"=="allure" goto :allure
set "SEL_M=smoke"
set "SEL_K="
if /i "%MODE%"=="smoke" set "SEL_M=smoke"
if /i "%MODE%"=="read" set "SEL_M=not mutating and not destructive and not online"
if /i "%MODE%"=="pay" set "SEL_M=not destructive"
if /i "%MODE%"=="destructive" set "SEL_M=destructive"
if /i "%MODE%"=="suite" set "SEL_M=f9%ARG%"
if /i "%MODE%"=="tc" set "SEL_K=tc_%ARG%"
if /i "%MODE%"=="full" set "SEL_M=smoke or not smoke"
if /i "%MODE%"=="rules" set "SEL_M=rules"
if /i "%MODE%"=="draft" set "SEL_M=draft"
if /i "%MODE%"=="defects" set "SEL_M=known_defect"

if /i "%MODE%"=="full" (
  echo.
  echo Che do full: chay het moi test, thanh toan that va rut can vi, khong hoi xac nhan.
  echo Sau khi chay xong can nap lai du lieu neu muon chay lai ^(run_edufams_update.cmd seed^).
  set "R9_ALLOW_PAYMENTS=1"
  set "R9_ALLOW_DESTRUCTIVE=1"
)
if /i "%MODE%"=="pay" (
  call :confirm PAY "Che do pay se tieu khoan phi that va tru tien trong vi EA cua con co vi lon nhat (Test Child One tren du lieu 21/10/2026)."
  if errorlevel 1 exit /b 2
  set "R9_ALLOW_PAYMENTS=1"
)
if /i "%MODE%"=="destructive" (
  call :confirm DRAIN "Che do destructive rut can vi EA cua mot con (Test Child Three tren du lieu 21/10/2026). Sau do phai reset du lieu bang tools\reset_payment_data.sql, sua ten con trong file cho khop du lieu moi."
  if errorlevel 1 exit /b 2
  set "R9_ALLOW_PAYMENTS=1"
  set "R9_ALLOW_DESTRUCTIVE=1"
)

rem Nap lai du lieu seed R9 truoc khi chay cac che do ghi du lieu (bo qua bang R9_NO_RESEED=1). Them chu each de nap lai truoc MOI test ghi du lieu.
set "DO_RESEED="
for %%M in (pay destructive full rules suite tc draft) do if /i "%MODE%"=="%%M" set "DO_RESEED=1"
if "%R9_NO_RESEED%"=="1" set "DO_RESEED="
if defined DO_RESEED (
  echo Dang nap lai du lieu seed R9 ...
  call reseed_r9.cmd
  if errorlevel 1 (echo Nap lai seed that bai. Chay lai voi R9_NO_RESEED=1 de bo qua buoc nay. & exit /b 1)
)
if "%R9_RESEED_EACH%"=="1" echo Che do each: nap lai seed truoc moi test ghi du lieu ^(se cham^).

where py >nul 2>&1 && (set "PY=py -3") || (set "PY=python")
if not exist ".venv\Scripts\python.exe" (
  echo Dang tao moi truong ao .venv ...
  %PY% -m venv .venv || goto :fail
)
set "VPY=.venv\Scripts\python.exe"
echo Dang cai thu vien ...
"%VPY%" -m pip install --quiet --disable-pip-version-check -r requirements.txt || goto :fail

if defined SEL_K goto :run_k
echo Chay: pytest -m "%SEL_M%" --browser-channel chrome %HEADED%
"%VPY%" -m pytest -m "%SEL_M%" --browser-channel chrome %HEADED%
set "RC=%ERRORLEVEL%"
goto :done

:run_k
echo Chay: pytest -k "%SEL_K%" --browser-channel chrome %HEADED%
"%VPY%" -m pytest -k "%SEL_K%" --browser-channel chrome %HEADED%
set "RC=%ERRORLEVEL%"

:done
echo.
echo pytest tra ve %RC%  (0 tat ca dat, 1 co test that bai, 5 khong co test nao duoc chon)
where allure >nul 2>&1
if not errorlevel 1 (
  echo Dang tao bao cao Allure mot file, kem video tung case ...
  call allure generate artifacts\allure-results -o artifacts\allure-report --clean --single-file
) else (
  echo Chua co lenh allure trong PATH nen chua tao bao cao Allure. Du lieu o artifacts\allure-results, video o artifacts\videos.
)
if exist "artifacts\allure-report\index.html" echo Bao cao Allure kem video:      artifacts\allure-report\index.html
echo Bao cao theo tung case R9 (case nao FAIL, loi da biet): artifacts\reports\r9_case_report.html
echo Ban Excel cua bao cao do: artifacts\reports\r9_case_report.csv
echo Bao cao theo ten test (pytest-html): artifacts\reports\report.html
if exist "artifacts\allure-report\index.html" start "" "artifacts\allure-report\index.html"
if exist "artifacts\reports\r9_case_report.html" (start "" "artifacts\reports\r9_case_report.html") else if exist "artifacts\reports\report.html" start "" "artifacts\reports\report.html"
exit /b %RC%

:allure
if exist "artifacts\allure-report\index.html" (
  start "" "artifacts\allure-report\index.html"
  exit /b 0
)
if exist "artifacts\allure-results" (
  call allure generate artifacts\allure-results -o artifacts\allure-report --clean --single-file
  start "" "artifacts\allure-report\index.html"
  exit /b 0
)
echo Chua co artifacts\allure-results. Hay chay test truoc.
exit /b 1

:checkurl
call set "U=%%%1%%"
if not defined U exit /b 0
echo %U%| findstr /i /c:"vercel" >nul && (echo.& echo %1=%U% la dia chi Vercel. Bo test R9 chi chay tren localhost, khong chay tren Vercel.& exit /b 1)
echo %U%| findstr /i /r /c:"//localhost[:/]" /c:"//localhost$" /c:"//127\.0\.0\.1" /c:"//\[::1\]" /c:"devtunnels" /c:"pinggy" >nul && exit /b 0
if "%R9_ALLOW_REMOTE%"=="1" exit /b 0
echo.& echo %1=%U% khong phai localhost. Bo test R9 chi chay tren may dang host he thong. May khac trong mang rieng: dat R9_ALLOW_REMOTE=1.
exit /b 1

:confirm
echo.
echo %~2
set "ANSWER="
set /p "ANSWER=Go %~1 de tiep tuc, phim khac de huy: "
if /i not "%ANSWER%"=="%~1" (
  echo Da huy, khong co gi bi thay doi.
  exit /b 1
)
exit /b 0

:fail
echo Cai dat that bai. Kiem tra da cai Python 3.9 tro len va pip co ket noi internet.
exit /b 1
