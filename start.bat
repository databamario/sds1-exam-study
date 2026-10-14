@echo off
REM One-click launcher for the SDS1 exam study app.
REM If the virtual environment does not exist yet, run the setup first
REM (see the README Quick start section).

if not exist ".venv\Scripts\python.exe" (
  echo No virtual environment found. Setting it up now...
  python -m venv .venv || goto :error
  call .venv\Scripts\activate
  pip install -r requirements.txt || goto :error
) else (
  call .venv\Scripts\activate
)

echo.
echo Starting the app at http://localhost:8501
echo Press Ctrl+C to stop.
echo.
streamlit run app.py
goto :eof

:error
echo.
echo Setup failed. Check that Python is installed and on your PATH,
echo then follow the README Quick start instructions.
pause
exit /b 1