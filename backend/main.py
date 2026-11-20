from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI(title="CORE 2050 HGIS & ABM Simulator API", version="1.0.0")


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "core2050_web",
        "domain": "core2050.soohwalee.com",
        "event": "2026 K-BALANCE Special Session (2026-12-10 Osong C&V Center)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
