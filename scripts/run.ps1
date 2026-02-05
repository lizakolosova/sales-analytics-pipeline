Write-Host "Starting Sales Analytics Pipeline (Windows)..." -ForegroundColor Green

Write-Host "`nStarting Docker services..." -ForegroundColor Yellow
docker-compose up -d postgres redis kafka zookeeper

Write-Host "`nWaiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "`n Core services started!" -ForegroundColor Green
Write-Host "`nTo start the application services, open 3 separate PowerShell windows:" -ForegroundColor Cyan
Write-Host "`n[Window 1 - API]" -ForegroundColor Yellow
Write-Host "python -m uvicorn src.api.main:app --reload"
Write-Host "`n[Window 2 - Kafka Producer]" -ForegroundColor Yellow
Write-Host "python -m src.kafka.producer"
Write-Host "`n[Window 3 - Dashboard]" -ForegroundColor Yellow
Write-Host "streamlit run src\dashboard\app.py"
Write-Host "`nOr run everything in Docker:" -ForegroundColor Cyan
Write-Host "docker-compose up -d"
Write-Host "`nAccess points:" -ForegroundColor Cyan
Write-Host "- API:       http://localhost:8000"
Write-Host "- Dashboard: http://localhost:8501"
Write-Host "`nTo stop all services:" -ForegroundColor Cyan
Write-Host "docker-compose down"
