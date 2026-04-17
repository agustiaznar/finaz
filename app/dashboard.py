import streamlit as st
import os

from infrastructure.db import init_db

# =========================
# CONFIG (SIEMPRE PRIMERO)
# =========================

st.set_page_config(
    page_title="Finaz",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# INIT (solo una vez)
# =========================

@st.cache_resource
def init():
    init_db()

init()

# =========================
# PATHS
# =========================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ACCOUNTS_DIR = os.path.join(BASE_DIR, "data", "accounts")

# =========================
# HELPERS
# =========================

@st.cache_data(ttl=5)
def get_profiles():
    if not os.path.exists(ACCOUNTS_DIR):
        return []

    return [
        f.replace("_ledger.xlsx", "")
        for f in os.listdir(ACCOUNTS_DIR)
        if f.endswith(".xlsx")
    ]

# =========================
# SESSION STATE
# =========================

profiles = get_profiles()

if "profile" not in st.session_state:
    st.session_state.profile = profiles[0] if profiles else None

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.title("⚙️ Finaz")

    if not profiles:
        st.warning("No hay perfiles disponibles")
        st.stop()

    if st.session_state.profile not in profiles:
        st.session_state.profile = profiles[0]

    index = profiles.index(st.session_state.profile)

    selected = st.selectbox("👤 Perfil", profiles, index=index)

    st.session_state.profile = selected

    st.caption(f"Perfil: {selected}")

    st.divider()

    st.markdown("### 📌 Navegación")

    st.page_link("pages/1_Resumen.py", label="📊 Resumen")
    st.page_link("pages/2_Categorias.py", label="🔥 Categorías")
    st.page_link("pages/3_Cashflow.py", label="💰 Cashflow")

    st.divider()
    st.caption("Finaz v1.0")

# =========================
# MAIN UI
# =========================

st.title("📊 FINAZ")

st.markdown("""
Bienvenido a tu sistema de análisis financiero.

Este dashboard te permite:

- Analizar ingresos y gastos  
- Ver evolución financiera  
- Detectar cambios en categorías  
- Gestionar tus clasificaciones  
""")

# =========================
# STATUS
# =========================

st.subheader("📌 Estado actual")

col1, col2 = st.columns(2)

col1.info(f"Perfil activo: **{st.session_state.profile}**")
col2.success("Sistema listo")

# =========================
# MINI DASHBOARD
# =========================

st.subheader("📈 Vista rápida")

mode = "Cloud" if os.environ.get("STREAMLIT_RUNTIME") else "Local"

col1, col2, col3 = st.columns(3)

col1.metric("Estado", "Activo")
col2.metric("Perfil", st.session_state.profile)
col3.metric("Modo", mode)

# =========================
# FOOTER
# =========================

st.markdown("---")
st.caption("Finaz — Financial Analytics System")