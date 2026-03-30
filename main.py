from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
import time

app = FastAPI(title="IoT API")

VALID_API_KEYS = {"esp32_001_abc123", "arduino_002_xyz789"}

class TelemetryPayload(BaseModel):
    device_id: str
    sensor_type: str
    value: float
    timestamp: int

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized: Invalid or Missing API Key"
        )
    return x_api_key

@app.post("/api/telemetry")
async def ingest_telemetry(
    payload: TelemetryPayload, 
    api_key: str = Depends(verify_api_key)
):
    return {
        "status": "success",
        "message": f"Data from {payload.device_id} securely ingested.",
        "processed_at": int(time.time())
    }


@app.get("/")
def read_root():
    return {"message": "Welcome to the IoT Telemetry API! Go to /docs to test the endpoints."}