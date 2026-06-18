import pandas as pd
import os
from src.features import extract_features

RAW_PATH = "datasets/raw/phishing.csv"
FALLBACK_PATH = "datasets/sample.csv"
OUT_PATH = "datasets/processed/data.csv"

def load_data():
    if os.path.exists(RAW_PATH):
        print("Usando dataset real:", RAW_PATH)
        return pd.read_csv(RAW_PATH)
    else:
        print("Dataset real no encontrado, usando fallback:", FALLBACK_PATH)
        return pd.read_csv(FALLBACK_PATH)

def build_dataset():
    df = load_data()

    rows = []

    for _, row in df.iterrows():
        url = row["url"]
        label = row["label"]

        feats = extract_features(url)
        feats["label"] = label

        rows.append(feats)

    out_df = pd.DataFrame(rows)
    os.makedirs("datasets/processed", exist_ok=True)
    out_df.to_csv(OUT_PATH, index=False)

    print("Dataset procesado:", OUT_PATH)

if __name__ == "__main__":
    build_dataset()
