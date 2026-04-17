import streamlit as st

from finaz.services.analytics.analytics_service import (
    get_enriched_monthly_series,
    get_expense_category_series
)

@st.cache_data(ttl=300, show_spinner=False)
def load_all_data(client_id, profile):
    if not client_id:
        raise ValueError("client_id inválido")

    df = get_enriched_monthly_series(client_id)
    df_cat = get_expense_category_series(client_id, profile)

    return df, df_cat