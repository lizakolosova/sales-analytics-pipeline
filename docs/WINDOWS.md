# Windows Troubleshooting Guide

All main setup instructions are in [README.md](../README.md). This page covers Windows-specific issues.

## Prerequisites

- Windows 10/11
- Python 3.12
- Docker Desktop (running)

## Common Issues

### 1. Kafka Module Error

**Error:**
```
ModuleNotFoundError: No module named 'kafka.vendor.six.moves'
```

**Fix:**
```powershell
pip uninstall kafka-python -y
pip install kafka-python-ng
```

**Why:** kafka-python doesn't support Python 3.12, use kafka-python-ng instead.

---

### 2. Streamlit Can't Import 'src'

**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Fix:**
```powershell
$env:PYTHONPATH = "$PWD"
streamlit run src/dashboard/app.py
```

**Why:** Streamlit needs the project root in PYTHONPATH.

---

### 3. Empty Dashboard

**Problem:** Dashboard shows "No data available" or zeros everywhere

**Fix:**
```powershell
python scripts/load_data.py
```

**Why:** Database is empty until you load the sample data.

---

### 4. Docker Connection Error

**Error:**
```
error during connect: ... is Docker running?
```

**Fix:**
1. Open Docker Desktop
2. Wait for "Docker Desktop is running" in system tray
3. Try again

**Why:** Docker engine must be running before starting containers.

---

### 5. Port Already in Use

**Error:**
```
Bind for 0.0.0.0:5432 failed: port is already allocated
```

**Fix:**
```powershell
# Check what's using the port
docker ps

# Stop other PostgreSQL containers
docker stop <container-name>

# Or restart everything
docker-compose down
docker-compose up -d postgres redis kafka zookeeper
```

**Why:** You might have other projects with PostgreSQL running.

---

### 6. Database Connection Failed

**Error:**
```
password authentication failed for user "postgres"
```

**Fix:**
```powershell
# Recreate database with fresh password
docker-compose down -v
docker-compose up -d postgres redis kafka zookeeper

# Wait 30 seconds, then retry
```

**Why:** Database password mismatch or database not fully initialized.

---

### 7. Permission Denied (PowerShell)

**Error:**
```
... cannot be loaded because running scripts is disabled
```

**Fix:**
Run PowerShell as Administrator, then:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Why:** Windows security policy restricts script execution.

---

## Quick Commands Reference

### View Logs
```powershell
docker-compose logs -f kafka-producer
docker-compose logs -f api
```

### Stop Everything
```powershell
docker-compose down
```

### Clean Restart
```powershell
docker-compose down -v
docker-compose up -d postgres redis kafka zookeeper
python scripts/load_data.py
```

### Check Running Containers
```powershell
docker ps
```

### Access Database
```powershell
docker exec -it sales-analytics-pipeline-postgres-1 psql -U postgres -d sales_analytics
```

### Check Kafka Events
```powershell
docker-compose logs -f kafka-producer
```

---

## Platform Differences

This project works on Windows, but some features require workarounds:

| Feature | Windows Status | Notes |
|---------|---------------|-------|
| Kafka | ✅ Works | Use kafka-python-ng |
| PostgreSQL | ✅ Works | Via Docker |
| Redis | ✅ Works | Via Docker |
| Streamlit | ✅ Works | Set PYTHONPATH |
| FastAPI | ✅ Works | Native support |
| Docker | ✅ Works | Docker Desktop required |

---

## Still Having Issues?

1. Check main [README.md](../README.md) for setup steps
2. Make sure you're in the project root directory
3. Verify Docker Desktop is running
4. Check all containers are up: `docker ps`
5. Review error messages carefully

---

**Environment Tested:**
- Windows 11 Pro
- Python 3.12.1
- Docker Desktop 4.x
- PowerShell 7.x

All components verified working in this environment.
