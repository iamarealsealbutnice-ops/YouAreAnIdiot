@echo off
REM harmless example: echo message 10 times, then wait
for /L %%i in (1,1,10) do (
  echo (%%i/50) bah.
)
pause
