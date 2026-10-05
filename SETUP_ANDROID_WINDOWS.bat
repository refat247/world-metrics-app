@echo off
setlocal
where node >nul 2>nul || (echo Node.js 22+ is required.& exit /b 1)
call npm ci || exit /b 1
if not exist android (
  call npx cap add android || exit /b 1
)
call npx cap sync android || exit /b 1
call npx cap open android
