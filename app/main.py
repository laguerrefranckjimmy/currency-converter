from fastapi import FastAPI, HTTPException
from app.schemas import ConvertRequest, ConvertResponse
from app.services import get_rate
from mangum import Mangum

app = FastAPI(title="Currency Converter Microservice", version="1.0.0")

PREFIX = "/currency-converter"  # matches API Gateway path

@app.get(f"{PREFIX}/health")
def health():
    return {"status": "ok"}

@app.post(f"{PREFIX}/convert", response_model=ConvertResponse)
def convert_currency(payload: ConvertRequest):
    try:
        rate = get_rate(payload.from_currency, payload.to_currency)
        converted = payload.amount * rate
        return ConvertResponse(rate=rate, converted_amount=round(converted, 2))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

handler = Mangum(app)
