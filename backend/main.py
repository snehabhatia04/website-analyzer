from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import requests
import asyncio

from performance_analyzer import analyze_performance
from security_analyzer import fetch_security_headers, check_https_certificate

app = FastAPI()

# Allow React frontend to call this backend
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic schema for incoming request validation
class URLRequest(BaseModel):
    url: HttpUrl


# API endpoint: POST /analyze
@app.post("/analyze")
async def analyze(request: URLRequest):
    try:
        url_str = str(request.url)

        # Measure Time To First Byte
        ttfb = measure_ttfb(url_str)

        # Fetch security headers (async)
        security_headers = fetch_security_headers(url_str) or {}


        # Fetch HTTPS certificate validity details
        cert_validity = check_https_certificate(url_str)

        # Analyze performance metrics via selenium-based performance_analyzer
        performance_metrics = analyze_performance(url_str)

        return {
            "url": url_str,
            "performance": {
                "ttfb_ms": ttfb,
                **performance_metrics
            },
            "security": {
                "https_certificate_validity": cert_validity,
                "secure_headers_status": security_headers
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Function to measure Time To First Byte
def measure_ttfb(url):
    response = requests.get(url)
    return round(response.elapsed.total_seconds() * 1000, 2)
