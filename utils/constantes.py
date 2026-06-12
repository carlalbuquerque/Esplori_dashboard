# ─── Paleta de Cores Explori ─────────────────────────────────────────────────
COR_PRIMARIA   = "#E07A2F"
COR_SECUNDARIA = "#B96A4A"
COR_VERDE      = "#4E582B"  
COR_NEUTRO     = "#ACB482"
COR_FUNDO      = "#F9F5F0"
COR_TEXTO      = "#1A1A1A"

# ─── Benchmarks de Negócio ───────────────────────────────────────────────────
BENCHMARK_CONVERSAO    = 0.35
BENCHMARK_SAVE         = 0.12
BENCHMARK_COMPARTILHAR = 0.04
BENCHMARK_USO_PROMO    = 0.50
BENCHMARK_RETENCAO     = 0.16

# ─── CSS Customizado ─────────────────────────────────────────────────────────
CSS_CUSTOMIZADO = f"""
<style>
    .block-container {{ background-color: {COR_FUNDO}; padding-top: 4.5rem; }}
    h1, h2, h3 {{ color: {COR_TEXTO}; }}
    .insight-box {{
        background: white;
        border-left: 4px solid {COR_PRIMARIA};
        padding: 0.75rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        color: {COR_TEXTO};
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }}
    .metric-card {{
        background: white;
        border-radius: 8px;
        padding: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .sidebar-title {{
        font-size: 0.85rem;
        font-weight: 600;
        color: #E07A2F;
        text-align: center;
        margin: 0;
        padding: 0.25rem 0;
    }}
    .sidebar-footer {{
        font-size: 0.7rem;
        color: {COR_TEXTO};
        text-align: center;
        margin-top: 1rem;
        line-height: 1.5;
    }}

    /* ── Navegação: botões retangulares ── */
    div[data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        border: none;
        border-radius: 6px;
        padding: 0.45rem 0.75rem;
        font-size: 0.82rem;
        font-weight: 500;
        text-align: center;
        background: transparent;
        color: {COR_TEXTO};
        transition: background 0.15s, color 0.15s;
        margin-bottom: 2px;
    }}
    div[data-testid="stSidebar"] .stButton > button:hover:not(:disabled) {{
        background: #F0E8DF;
        color: {COR_PRIMARIA};
    }}
    /* botão ativo (primary + disabled) */
    div[data-testid="stSidebar"] button[data-testid="baseButton-primary"],
    div[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:disabled,
    div[data-testid="stSidebar"] button[data-testid="baseButton-primary"][disabled] {{
        background: {COR_PRIMARIA} !important;
        background-color: {COR_PRIMARIA} !important;
        color: white !important;
        border: none !important;
        opacity: 1 !important;
        font-weight: 600;
        cursor: default;
        box-shadow: none !important;
    }}
</style>
"""
