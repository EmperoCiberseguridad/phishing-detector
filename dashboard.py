import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SOC Dashboard - Phishing Detector", layout="wide")

st.title("SOC Dashboard - Phishing Detection System")

API_URL = "http://127.0.0.1:8000/scan"

# historial en sesión
if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input("URL a analizar:")

    if st.button("Analizar"):
        if url:
            try:
                response = requests.post(API_URL, json={"url": url})
                data = response.json()

                # guardar en historial
                st.session_state.history.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "url": data["url"],
                    "verdict": data["verdict"],
                    "risk_score": data["risk_score"],
                    "confidence": data["confidence"]
                })

            except Exception as e:
                st.error(f"Error conectando con API: {e}")

with col2:
    st.subheader("Estado del sistema")
    st.write("API: http://127.0.0.1:8000")

# métricas globales
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    st.subheader("Métricas")

    avg_risk = df["risk_score"].mean()
    total = len(df)
    phishing_count = len(df[df["verdict"] == "PHISHING"])

    st.metric("Total análisis", total)
    st.metric("Riesgo promedio", round(avg_risk, 2))
    st.metric("Phishing detectado", phishing_count)

    st.subheader("Historial de eventos")

    def color_verdict(val):
        if val == "PHISHING":
            return "background-color: #ffcccc"
        return "background-color: #ccffcc"

    st.dataframe(df.style.applymap(color_verdict, subset=["verdict"]))

else:
    st.info("No hay eventos aún. Analiza una URL para empezar.")
