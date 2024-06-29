@REM @echo off
@REM echo System Information:
@REM systeminfo
@REM echo.
@REM echo Memory Information:
@REM systeminfo | findstr /C:"Total Physical Memory"
@REM echo.
@REM echo Processor Information:
@REM wmic cpu get name,numberofcores,numberoflogicalprocessors
@REM echo.
@REM echo Display Information:
@REM wmic path win32_videocontroller get caption,deviceid,adapterram
@REM echo.
@REM echo MAC Address:
@REM getmac
@REM pause

@echo off
set OUTPUT_FILE=system_info.txt

echo System Information: > %OUTPUT_FILE%
systeminfo >> %OUTPUT_FILE%
echo. >> %OUTPUT_FILE%
echo Memory Information: >> %OUTPUT_FILE%
systeminfo | findstr /C:"Total Physical Memory" >> %OUTPUT_FILE%
echo. >> %OUTPUT_FILE%
echo Processor Information: >> %OUTPUT_FILE%
wmic cpu get name,numberofcores,numberoflogicalprocessors >> %OUTPUT_FILE%
echo. >> %OUTPUT_FILE%
echo Display Information: >> %OUTPUT_FILE%
wmic path win32_videocontroller get caption,deviceid,adapterram >> %OUTPUT_FILE%
echo. >> %OUTPUT_FILE%
echo MAC Address: >> %OUTPUT_FILE%
getmac >> %OUTPUT_FILE%
echo. >> %OUTPUT_FILE%

echo Information has been saved to %OUTPUT_FILE%
pause
