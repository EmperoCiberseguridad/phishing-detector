from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import joblib
import os

from src.features import extract_features

app = FastAPI(title="Phishing Detector SOC API")

MODEL_PATH = "models/model.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model not found. Run: python -m src.train")

model = joblib.load(MODEL_PATH)

#IMPORTANTE: orden fijo de features (evita bugs silenciosos)
FEATURE_ORDER = [
    "url_length",
    "subdomain_count",
    "has_https",
    "has_ip",
    "has_at_symbol",
    "has_dash",
    "num_params"
]


class URLRequest(BaseModel):
    url: HttpUrl


def explain(features: dict):
    reasons = []

    if features["has_ip"]:
        reasons.append("High risk: IP-based host detected")

    if features["has_at_symbol"]:
        reasons.append("Medium risk: '@' symbol used to obscure domain")

    if not features["has_https"]:
        reasons.append("Medium risk: no HTTPS encryption")

    if features["subdomain_count"] > 2:
        reasons.append("Medium risk: excessive subdomain chaining")

    return reasons


@app.post("/scan")
def scan(data: URLRequest):
    feats = extract_features(str(data.url))

    # orden estable de features
    X = [[feats[f] for f in FEATURE_ORDER]]

    prob = model.predict_proba(X)[0][1]

    score = min(100, max(0, round(prob * 100, 2)))

    reasons = explain(feats)

    return {
        "url": str(data.url),
        "verdict": "PHISHING" if score > 50 else "LEGITIMATE",
        "risk_score": score,
        "confidence": round(prob, 3),
        "reasons": reasons
    }


@app.get("/health")
def health():
    return {"status": "ok"}
