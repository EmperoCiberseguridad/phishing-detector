import joblib

MODEL_PATH = "models/model.pkl"

def predict(url: str):
    model = joblib.load(MODEL_PATH)
    return model.predict([url])[0]

if __name__ == "__main__":
    test_url = "http://secure-login-bank.com"
    result = predict(test_url)

    print("URL:", test_url)
    print("Predicción:", "Phishing" if result == 1 else "Legítima")
