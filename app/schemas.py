from pydantic import BaseModel

class ConvertRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class ConvertResponse(BaseModel):
    rate: float
    converted_amount: float
