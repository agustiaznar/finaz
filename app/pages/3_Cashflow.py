import streamlit as st

from infrastructure.db import get_connection
from services.cache_service import load_all_data
from services.charts.charts_cashflow import (
    cashflow_category,
    cashflow_monthly
)

st.set_page_config(page_title="Cashflow", layout="wide")

# =========================
# PROFILE GLOBAL
# =========================

profile = st.session_state.get("profile")

if not profile:
    st.warning("Selecciona un perfil")
    st.stop()

# =========================
# HELPERS
# =========================

def get_client_id(name):
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM clients WHERE name=?",
        (name,)
    ).fetchone()
    conn.close()
    return row[0] if row else None

# =========================
# DATA
# =========================

client_id = get_client_id(profile)

try:
    with st.spinner("Cargando cashflow..."):
        _, df_cat = load_all_data(client_id, profile)
except Exception:
    st.error("Error cargando datos")
    st.stop()

# =========================
# UI
# =========================

st.title("💰 Cashflow")

st.subheader("Cashflow por categoría")
st.altair_chart(cashflow_category(df_cat), width="stretch")

st.subheader("Cashflow mensual")
st.altair_chart(cashflow_monthly(df_cat), width="stretch")