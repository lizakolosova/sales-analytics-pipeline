Write-Host "Setting up Sales Analytics Pipeline for Windows..." -ForegroundColor Green

$ErrorActionPreference = "Stop"

Write-Host "`nChecking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host $pythonVersion

if (-not (Test-Path ".env")) {
    Write-Host "`nCreating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
Write-Host "Note: Skipping Apache Airflow (requires Python <3.12)" -ForegroundColor Red

pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install kafka-python==2.0.2
pip install sqlalchemy==2.0.23
pip install psycopg2-binary==2.9.9
pip install redis==5.0.1
pip install streamlit==1.29.0
pip install plotly==5.18.0
pip install pandas==2.1.3
pip install requests==2.31.0
pip install python-dotenv==1.0.0

Write-Host "`nGenerating sample dataset..." -ForegroundColor Yellow
python scripts\generate_dataset.py

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Make sure Docker Desktop is running"
Write-Host "2. Run: docker-compose up -d postgres redis kafka zookeeper"
Write-Host "3. Run: python -c `"from src.database.models import init_db; from config.settings import get_settings; init_db(get_settings().database_url)`""
Write-Host "4. Start services:"
Write-Host "   - API:       python -m uvicorn src.api.main:app --reload"
Write-Host "   - Producer:  python -m src.kafka.producer"
Write-Host "   - Dashboard: streamlit run src\dashboard\app.py"
Write-Host "`nAccess points:" -ForegroundColor Cyan
Write-Host "- API:       http://localhost:8000"
Write-Host "- Dashboard: http://localhost:8501"
