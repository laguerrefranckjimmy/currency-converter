import requests
import os
import time

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest"
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))

# Simple in-memory cache
_cache = {}

def get_rate(from_currency: str, to_currency: str) -> float:
    key = f"{from_currency.upper()}_{to_currency.upper()}"
    now = time.time()

    # Check cache
    if key in _cache:
        rate, timestamp = _cache[key]
        if now - timestamp < CACHE_TTL:
            return rate

    # Fetch from API
    response = requests.get(f"{BASE_URL}/{from_currency.upper()}")
    data = response.json()
    if data["result"] != "success":
        raise ValueError("Failed to fetch exchange rates")

    rate = data["conversion_rates"].get(to_currency.upper())
    if not rate:
        raise ValueError("Invalid currency code")

    # Update cache
    _cache[key] = (rate, now)
    return rate
