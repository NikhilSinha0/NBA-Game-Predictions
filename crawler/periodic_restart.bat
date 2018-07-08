@echo off
SET /P first="First season start year: "
SET /P last="Last season start year: "
for /l %%x in (%first%, 1, %last%) do (
SETLOCAL EnableDelayedExpansion
set /a next=%%x+1
python main.py 10/17/%%x 7/1/!next!
ENDLOCAL
)