from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ConvertRequest, ConvertResponse
from app.services import get_rate
from mangum import Mangum

# FastAPI app
app = FastAPI(
    title="Currency Converter Microservice",
    version="1.0.0"
)

# Prefix for API Gateway
PREFIX = "/currency-converter"

# === CORS Configuration ===
# Add your frontend domains here
origins = [
    "https://francklab.fyi",
    "http://localhost:5173",  # for local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS", "GET"],  # support preflight + GET endpoints
    allow_headers=["Content-Type"],
)

# === Health endpoint ===
@app.get(f"{PREFIX}/health")
def health():
    return {"status": "ok"}

# === Currency conversion endpoint ===
@app.post(f"{PREFIX}/convert", response_model=ConvertResponse)
def convert_currency(payload: ConvertRequest):
    try:
        rate = get_rate(payload.from_currency, payload.to_currency)
        converted = payload.amount * rate
        return ConvertResponse(rate=rate, converted_amount=round(converted, 2))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# === Mangum handler for Lambda ===
handler = Mangum(app)