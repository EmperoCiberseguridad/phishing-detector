import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

DATA_PATH = "datasets/sample.csv"
MODEL_PATH = "models/model.pkl"

def train():
    df = pd.read_csv(DATA_PATH)

    X = df["url"]
    y = df["label"]

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Modelo entrenado y guardado en:", MODEL_PATH)

if __name__ == "__main__":
    train()
