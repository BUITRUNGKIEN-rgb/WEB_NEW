@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"
title AI02 V13 - Day code len GitHub an toan

echo =============================================
echo    AI02 V13 - UNETI12 ODD3 - GitHub
 echo =============================================
echo.
echo CHI DAY MA NGUON. KHONG DAY DATASET, MODEL, SECRETS.
echo Can tao repository TRONG tren GitHub truoc.
echo KHONG tick: Add README / Add .gitignore / Choose a license.
echo.

where git >nul 2>&1
if errorlevel 1 (
 echo [LOI] May chua cai Git hoac chua them Git vao PATH.
 echo Tai Git: https://git-scm.com/downloads/win
 goto :fail
)

if exist ".git" (
 echo [CHU Y] Thu muc da co .git, script se KHONG thay doi remote hay ghi de lich su.
 echo Neu can, hay day bang VS Code / lenh git thu cong.
 goto :fail
)

set "PY_CMD="
where py >nul 2>&1
if not errorlevel 1 set "PY_CMD=py -3"
if not defined PY_CMD (
  where python >nul 2>&1
  if not errorlevel 1 set "PY_CMD=python"
)
if not defined PY_CMD (
 echo [LOI] Chua co Python de kiem tra file truoc khi day.
 goto :fail
)

echo NHAP LINK REPO GITHUB MOI (vd: https://github.com/USERNAME/AI02-UNETI12-ODD3.git)
set /p "REPO_URL=GitHub URL: "
if not defined REPO_URL (
 echo [LOI] Ban chua nhap URL repository.
 goto :fail
)

echo %REPO_URL% | findstr /b /c:"https://github.com/" >nul
if errorlevel 1 (
 echo [LOI] Chi nhan link https://github.com/...
 goto :fail
)

git init
if errorlevel 1 goto :gitfail
git branch -M main
if errorlevel 1 goto :gitfail

git add .
if errorlevel 1 goto :gitfail

%PY_CMD% KIEM_TRA_GITHUB_AN_TOAN.py
if errorlevel 1 (
 echo [BLOCK] Phat hien rui ro; DA DUNG. KHONG COMMIT, KHONG PUSH.
 goto :fail
)

echo.
echo ===== FILE SAP DUOC DAY =====
git status --short
echo.
set /p "CONFIRM=Ban da kiem tra danh sach, tiep tuc? (Y/N): "
if /I not "%CONFIRM%"=="Y" (
 echo [STOP] Khong push.
 goto :fail
)

git commit -m "AI02 V13 - UNETI12 ODD3"
if errorlevel 1 (
 echo [LOI] Khong commit duoc. Kiem tra user.name / user.email Git.
 echo   git config --global user.name "Your Name"
 echo   git config --global user.email "you@example.com"
 goto :fail
)

git remote add origin "%REPO_URL%"
if errorlevel 1 goto :gitfail

git push -u origin main
if errorlevel 1 (
 echo.
 echo [LOI] PUSH CHUA THANH CONG. Du lieu may ban van an toan.
 echo Neu repo GitHub co san README, push co the bi tu choi do lich su khac nhau.
 echo KHONG su dung git push --force. Tao repo TRONG hoac xu ly xung dot thu cong.
 echo Neu loi xac thuc, dang nhap GitHub trong cua so trinh duyet do Git mo.
 goto :fail
)

echo.
echo [OK] PUSH HOAN TAT. Ban hay mo link repository de kiem tra.
pause
exit /b 0

:gitfail
echo [LOI] Lenh Git that bai. Xem dong loi ben tren.
:fail
echo Khong co dataset hay model nao bi xoa, ghi de hoac di chuyen.
pause
exit /b 1
