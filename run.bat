@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting SilvaLoader...
python main.py

pause
