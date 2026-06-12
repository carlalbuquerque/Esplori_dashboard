# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 1 — CONFIGURAÇÃO DA PÁGINA
# Deve ser sempre a primeira chamada Streamlit do arquivo.
# ─────────────────────────────────────────────────────────────────────────────
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Esplori — Dashboard Estabelecimento de Restaurantes",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 2 — IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
from utils.constantes import CSS_CUSTOMIZADO
from utils.dados import calcular_kpis, carregar_dados
import views.benchmarking   as tela_benchmarking
import views.engajamento    as tela_engajamento
import views.perfil_publico as tela_perfil_publico
import views.promocoes      as tela_promocoes
import views.retencao       as tela_retencao
# `views.visao_geral` foi removida; não importamos mais a tela Visão Geral.

# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 3 — CSS CUSTOMIZADO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(CSS_CUSTOMIZADO, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 4 — CARGA E PREPARAÇÃO DE DADOS
# ─────────────────────────────────────────────────────────────────────────────
try:
    dados = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

_u, _e, _c, _ec, checkins, interacoes, promocoes = dados
kpis = calcular_kpis(checkins, interacoes, promocoes)

# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 5 — SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Perfil do Público"

_OPCOES = [
    "Perfil do Público",
    "Engajamento",
    "Retenção",
    "Promoções",
    "Benchmarking",
]

with st.sidebar:
    _logo_path = os.path.join(BASE_DIR, "utils", "assets", "marca2-colorido.png")
    if os.path.exists(_logo_path):
        with open(_logo_path, "rb") as _f:
            st.image(_f.read(), use_container_width=True)
    st.markdown('<div class="sidebar-title">Dashboard para Estabelecimento de Restaurantes</div>', unsafe_allow_html=True)
    st.divider()

    for _op in _OPCOES:
        _ativo = st.session_state["pagina"] == _op
        if _ativo:
            st.button(_op, key=f"nav_{_op}", use_container_width=True, type="primary",)
        else:
            if st.button(_op, key=f"nav_{_op}", use_container_width=True):
                st.session_state["pagina"] = _op
                st.rerun()

    st.markdown(
        '<div class="sidebar-footer">Esplori &copy; 2025–2026<br>Região Metropolitana do Recife</div>',
        unsafe_allow_html=True,
    )

pagina = st.session_state["pagina"]

# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 6 — ROTEAMENTO DE PÁGINAS
# ─────────────────────────────────────────────────────────────────────────────
_PAGINAS = {
    "Perfil do Público": tela_perfil_publico,
    "Engajamento":       tela_engajamento,
    "Retenção":          tela_retencao,
    "Promoções":         tela_promocoes,
    "Benchmarking":      tela_benchmarking,
}

_PAGINAS[pagina].render(dados, kpis)
