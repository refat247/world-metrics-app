@echo off
setlocal
call npx cap sync android || exit /b 1
call npx cap open android
