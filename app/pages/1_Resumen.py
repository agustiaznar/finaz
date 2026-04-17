import streamlit as st

from infrastructure.db import get_connection
from services.cache_service import load_all_data
from services.kpis.kpi_service import compute_kpis
from services.charts.charts_monthly import global_finance_summary
from services.charts_summary import render_finance_summary_card

st.set_page_config(page_title="Resumen", layout="wide")

# =========================
# PROFILE GLOBAL
# =========================

profile = st.session_state.get("profile")

if not profile:
    st.warning("Selecciona un perfil en el dashboard")
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
    with st.spinner("Cargando datos..."):
        df, df_cat = load_all_data(client_id, profile)
except Exception as e:
    st.error("Error cargando datos")
    st.exception(e)
    st.stop()

# =========================
# KPIs
# =========================

kpis = compute_kpis(df, df_cat)

# =========================
# UI
# =========================

st.title("📊 Resumen")

render_finance_summary_card(kpis)

st.subheader("Resumen global")

st.altair_chart(
    global_finance_summary(
        kpis.get("balance"),
        kpis.get("total_income"),
        kpis.get("total_expense")
    ),
    width="stretch"
)