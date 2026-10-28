@echo off
rem Don dep roi nap lai du lieu seed R9 ve trang thai ban dau (chay trong thu muc r9_automation).
rem Chi dong co ma R9- bi xoa va nap lai. Ket qua ghi vao cleanup_output.txt va seed_output.txt.
setlocal
where docker >nul 2>nul || (echo Khong tim thay docker & exit /b 2)
type tools\seed_r9_cleanup.sql | docker exec -i edufams-qa-sqlserver bash -c "/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P \"$MSSQL_SA_PASSWORD\" -C -b -I" > cleanup_output.txt 2>&1
if errorlevel 1 (echo Cleanup loi, xem cleanup_output.txt & exit /b 1)
type tools\seed_r9_data.sql | docker exec -i edufams-qa-sqlserver bash -c "/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P \"$MSSQL_SA_PASSWORD\" -C -b -I" > seed_output.txt 2>&1
if errorlevel 1 (echo Nap du lieu loi, xem seed_output.txt & exit /b 1)
echo Da nap lai du lieu R9. Xem seed_output.txt de doi chieu.
endlocal
