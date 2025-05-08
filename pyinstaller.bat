REM pyinstaller.bat
@echo on

REM 0) Change to the directory of this script
cd /d %~dp0

REM 1) Remove the old build
del /q _internal\*.*
for /d %%D in (_internal\*) do (
    if /I "%%~nD" NEQ "images" (
        rd /s /q "%%D"
    )
)
if exist Dateiablage.exe (
    del /q Dateiablage.exe
)

REM 2) Run PyInstaller with Dateiablage.spec
python -m PyInstaller --noconfirm Dateiablage.spec

REM 3) Copy Dateiablage.exe to the current directory
xcopy /y /i /e "dist\Dateiablage\Dateiablage.exe" "%~dp0"

REM 4) Copy (or merge) the images folder to _internal\images
xcopy /y /i /e "dist\Dateiablage\_internal\_internal\images" "%~dp0\_internal\images"

REM 5)  Remove the _internal\_internal directory
if exist dist\Dateiablage\_internal\_internal (
    rd /s /q dist\Dateiablage\_internal\_internal
)

REM 6) Copy/merge the rest of the _internal directory to _internal
xcopy /y /i /e "dist\Dateiablage\_internal" "%~dp0\_internal"

REM 7) Remove the dist directory
if exist dist (
    rd /s /q dist
)

REM 8) Remove the build directory
if exist build (
    rd /s /q build
)

REM 9) Remove the redundant _internal directory
if exist _internal\_internal (
    rd /s /q _internal\_internal
)