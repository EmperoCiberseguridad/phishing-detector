import joblib
from src.features import extract_features

MODEL_PATH = "models/model.pkl"

def predict(url: str):
    model = joblib.load(MODEL_PATH)
    feats = extract_features(url)

    X = [list(feats.values())]
    return model.predict(X)[0]

if __name__ == "__main__":
    url = "http://secure-login-bank.com"
    result = predict(url)

    print("URL:", url)
    print("Resultado:", "PHISHING" if result == 1 else "LEGÍTIMO")
