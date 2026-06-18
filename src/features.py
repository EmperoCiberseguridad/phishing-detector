import re
from urllib.parse import urlparse

def extract_features(url: str):
    parsed = urlparse(url)

    features = {}

    # Longitud total
    features["url_length"] = len(url)

    # Número de subdominios
    features["subdomain_count"] = parsed.netloc.count(".") - 1

    # Tiene HTTPS
    features["has_https"] = 1 if parsed.scheme == "https" else 0

    # Tiene IP en vez de dominio
    features["has_ip"] = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+", parsed.netloc) else 0

    # Tiene símbolos sospechosos
    features["has_at_symbol"] = 1 if "@" in url else 0
    features["has_dash"] = 1 if "-" in parsed.netloc else 0

    # Cantidad de parámetros
    features["num_params"] = len(parsed.query.split("&")) if parsed.query else 0

    return features
