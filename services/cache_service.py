import streamlit as st

from services.analytics.analytics_service import (
    get_enriched_monthly_series,
    get_expense_category_series
)

# =========================
# CACHE GLOBAL
# =========================

@st.cache_data(ttl=300, show_spinner=False)
def load_all_data(client_id, profile):
    """
    Carga todos los datos necesarios (cacheado)

    Args:
        client_id: ID del cliente
        profile: nombre del perfil

    Returns:
        df, df_cat
    """

    if not client_id:
        raise ValueError("client_id inválido")

    df = get_enriched_monthly_series(client_id)
    df_cat = get_expense_category_series(client_id, profile)

    return df, df_cat