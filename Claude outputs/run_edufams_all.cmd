@echo off
rem EduFAMS launcher: backend (Docker) and frontend (Vite) from one place.
rem Put this file in the folder that holds edufams-backend and edugovernment-frontend.
rem   run_edufams_all.cmd             start the backend, wait for the gateway, then start both frontend apps
rem   run_edufams_all.cmd be          backend only
rem   run_edufams_all.cmd fe          frontend only, no Docker needed
rem   run_edufams_all.cmd mockpass    start MockPass, the Singpass simulator that e-service login needs
rem   run_edufams_all.cmd status      what is running
rem   run_edufams_all.cmd down        stop the backend, close the two frontend windows yourself
rem   add the word lan at the end to let other machines open the apps, for example run_edufams_all.cmd up lan
rem To point the frontend at a backend on another machine, set BACKEND_URL first:
rem   set BACKEND_URL=http://26.1.2.3:5273
rem   run_edufams_all.cmd fe
setlocal EnableExtensions EnableDelayedExpansion

set "MODE=up"
set "LAN="
for %%A in (%*) do (
  set "ARGV=%%~A"
  if /i "!ARGV!"=="lan" (set "LAN=1") else (set "MODE=!ARGV!")
)

set "BASE=%~dp0"
set "BE="
set "FE="
if exist "%BASE%edufams-backend\docker-compose.yml" set "BE=%BASE%edufams-backend"
if not defined BE if exist "%BASE%copy\edufams-backend\docker-compose.yml" set "BE=%BASE%copy\edufams-backend"
if exist "%BASE%edugovernment-frontend\package.json" set "FE=%BASE%edugovernment-frontend"
if not defined FE if exist "%BASE%copy\edugovernment-frontend\package.json" set "FE=%BASE%copy\edugovernment-frontend"
if not defined BE echo Backend folder edufams-backend not found next to this file.
if not defined FE echo Frontend folder edugovernment-frontend not found next to this file.

set "COMPOSE=docker-compose.yml"
if defined BE if exist "%BE%\deploy\qa\docker-compose.yml" set "COMPOSE=deploy\qa\docker-compose.yml"

if /i "%MODE%"=="up" goto :do_up
if /i "%MODE%"=="be" goto :do_be
if /i "%MODE%"=="fe" goto :do_fe
if /i "%MODE%"=="mockpass" goto :do_mockpass
if /i "%MODE%"=="status" goto :do_status
if /i "%MODE%"=="down" goto :do_down
echo Unknown command: %MODE%
echo Use one of: up, be, fe, mockpass, status, down. Add lan to share the apps with other machines.
exit /b 1

:do_up
call :backend || exit /b 1
call :frontend || exit /b 1
exit /b 0

:do_be
call :backend
exit /b %ERRORLEVEL%

:do_fe
call :frontend
exit /b %ERRORLEVEL%

:backend
if not defined BE exit /b 1
if /i "%PROCESSOR_ARCHITECTURE%"=="ARM64" (
  echo This computer is ARM64. SQL Server in Docker crashes here, so the backend cannot run on this machine.
  echo Run the backend on an x64 computer, then on this one use: set BACKEND_URL=http://IP-of-that-computer:5273
  echo and: run_edufams_all.cmd fe
  exit /b 1
)
where docker >nul 2>&1 || (
  echo Docker is not installed. Install Docker Desktop and run this file again.
  exit /b 1
)
docker info >nul 2>&1 || (
  echo Docker is installed but not running. Start Docker Desktop and run this file again.
  exit /b 1
)
echo Backend folder: %BE%
echo Compose file: %COMPOSE%
pushd "%BE%"
docker compose -f %COMPOSE% up -d --build
if errorlevel 1 (
  popd
  echo The backend failed to start. See the messages above.
  exit /b 1
)
popd
echo Waiting for the gateway on http://localhost:5273 ...
set /a TRIES=0
:wait_gateway
curl.exe -fs -o nul http://localhost:5273/health >nul 2>&1
if not errorlevel 1 goto :gateway_ok
set /a TRIES+=1
if !TRIES! GEQ 90 (
  echo The gateway did not answer after 15 minutes. Run: docker compose -f %COMPOSE% logs --tail 100
  exit /b 1
)
timeout /t 10 /nobreak >nul
goto :wait_gateway
:gateway_ok
echo Backend is up. ApiGateway: http://localhost:5273  Swagger: http://localhost:5273/swagger
exit /b 0

:frontend
if not defined FE exit /b 1
where node >nul 2>&1 || (
  echo Node.js is not installed. Install Node.js 22 from nodejs.org and run this file again.
  exit /b 1
)
where npm >nul 2>&1 || (
  echo npm is not installed. Reinstall Node.js 22 from nodejs.org.
  exit /b 1
)
set "NV="
for /f "tokens=1 delims=." %%V in ('node --version') do set "NV=%%V"
set "NV=!NV:v=!"
if !NV! LSS 22 echo WARNING: Node.js !NV! found, the frontend needs 22.12 or newer.
if not exist "%FE%\node_modules" (
  echo Installing frontend packages with npm ci. This takes a few minutes.
  pushd "%FE%"
  call npm ci
  if errorlevel 1 (
    popd
    echo npm ci failed. See the messages above.
    exit /b 1
  )
  popd
)
if defined BACKEND_URL set "VITE_BACK_END_URL=%BACKEND_URL%"
if not defined VITE_MOCKPASS_BASE_URL set "VITE_MOCKPASS_BASE_URL=http://localhost:5156/singpass/login"
echo Backend URL used by the apps: !VITE_BACK_END_URL!
echo MockPass URL used by e-service: %VITE_MOCKPASS_BASE_URL%
echo If the line above shows nothing for the backend, the .env file of each app is used, normally http://localhost:5273.
set "EXTRA="
if defined LAN set "EXTRA=-- --host"
start "EduFAMS admin-portal 5173" /d "%FE%" cmd /k npm run dev:admin %EXTRA%
start "EduFAMS e-service 5174" /d "%FE%" cmd /k npm run dev:eservice %EXTRA%
timeout /t 10 /nobreak >nul
start "" http://localhost:5173
start "" http://localhost:5174
echo.
echo Frontend started in two new windows.
echo   Admin portal  http://localhost:5173
echo   E-service     http://localhost:5174
if defined LAN echo Other machines open http://IP-of-this-computer:5173 and :5174. Allow those ports in Windows Firewall first.
exit /b 0

:do_mockpass
if not defined BE exit /b 1
where node >nul 2>&1 || (
  echo Node.js is not installed. Install Node.js from nodejs.org.
  exit /b 1
)
if not exist "%BE%\Simulation\mockpass\node_modules" (
  pushd "%BE%\Simulation\mockpass"
  call npm install
  popd
)
start "EduFAMS MockPass" /d "%BE%\Simulation\mockpass" cmd /k npm start
echo MockPass started in a new window, the Singpass login page is http://localhost:5156/singpass/login
exit /b 0

:do_status
if defined BE (
  pushd "%BE%"
  docker compose -f %COMPOSE% ps
  popd
)
for %%P in (5273 5173 5174) do (
  curl.exe -s -o nul --max-time 3 http://localhost:%%P/ >nul 2>&1 && (echo Port %%P answers) || (echo Port %%P no answer)
)
exit /b 0

:do_down
if not defined BE exit /b 1
pushd "%BE%"
docker compose -f %COMPOSE% down
popd
echo Backend stopped. Close the two frontend windows by hand.
exit /b 0
