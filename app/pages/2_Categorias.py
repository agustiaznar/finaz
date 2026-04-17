import streamlit as st

from infrastructure.db import get_connection
from services.cache_service import load_all_data
from services.categories.category_engine import normalize
from services.categories.category_persistence import save_concept_category
from services.charts.charts_categories import (
    expense_category_delta,
    expense_category_ranking
)

st.set_page_config(page_title="Categorías", layout="wide")

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
    with st.spinner("Cargando categorías..."):
        _, df_cat = load_all_data(client_id, profile)
except Exception:
    st.error("Error cargando categorías")
    st.stop()

# =========================
# UI
# =========================

st.title("🔥 Categorías")

st.altair_chart(expense_category_delta(df_cat), width="stretch")
st.altair_chart(expense_category_ranking(df_cat), width="stretch")

# =========================
# EDITOR
# =========================

df_cat["concept"] = df_cat["description"].apply(normalize)

df_edit = (
    df_cat
    .groupby("concept")
    .agg({"amount": "sum", "category": "first"})
    .reset_index()
)

edited_df = st.data_editor(df_edit, width="stretch")

if st.button("💾 Guardar"):
    for _, row in edited_df.iterrows():
        save_concept_category(
            row["concept"],
            str(row["category"]).strip().lower(),
            profile
        )

    st.success("Guardado")
    st.cache_data.clear()
    st.rerun()