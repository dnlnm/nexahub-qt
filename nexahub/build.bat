@echo off
echo Building NexaHub with Nuitka...
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Build with Nuitka
echo.
echo Converting icon to ICO...
python -c "from PySide6.QtGui import QImage, QIcon; from PySide6.QtWidgets import QApplication; import sys; app = QApplication(sys.argv); img = QImage('resources/icon.png'); img.save('resources/icon.ico')"

echo.
echo.
echo Compiling with Nuitka...
python -m nuitka --standalone --enable-plugin=pyside6 ^
    --windows-disable-console ^
    --windows-icon-from-ico=resources\icon.ico ^
    --include-data-dir=resources=resources ^
    --company-name="NexaHub" ^
    --product-name="NexaHub" ^
    --file-version=1.0.0 ^
    --product-version=1.0.0 ^
    --output-dir=dist ^
    --output-filename=NexaHub ^
    main.py

if %ERRORLEVEL% == 0 (
    echo.
    echo Build successful!
    echo Output: dist\main.dist\NexaHub.exe
) else (
    echo.
    echo Build failed!
    exit /b 1
)
