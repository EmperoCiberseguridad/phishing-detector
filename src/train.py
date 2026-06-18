import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

DATA_PATH = "datasets/processed/data.csv"
MODEL_PATH = "models/model.pkl"

def train():
    df = pd.read_csv(DATA_PATH)

    X = df.drop("label", axis=1)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Modelo entrenado correctamente")
    print("Accuracy:", acc)

if __name__ == "__main__":
    train()
