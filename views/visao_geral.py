import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.constantes import (
    BENCHMARK_COMPARTILHAR,
    BENCHMARK_CONVERSAO,
    BENCHMARK_SAVE,
    BENCHMARK_USO_PROMO,
    COR_FUNDO,
    COR_NEUTRO,
    COR_PRIMARIA,
    COR_SECUNDARIA,
    COR_TEXTO,
    COR_VERDE,
)


def render(dados: tuple, kpis: dict) -> None:
    _u, _e, _c, _ec, _ch, _i, _p = dados

    st.markdown(
        '<div style="font-size:2.25rem;font-weight:700;color:#2D2D2D;'
        'line-height:1.2;margin-bottom:0.3rem;">Visão Geral</div>',
        unsafe_allow_html=True,
    )
    st.caption("Resumo executivo dos principais indicadores do seu restaurante na plataforma Explori.")

    # ── Cards de KPI ────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Visualizações", f"{kpis['total_views']:,}")
    c2.metric("Check-ins", f"{kpis['total_checkins']:,}")
    c3.metric(
        "Conversão",
        f"{kpis['taxa_conversao']:.1%}",
        delta=f"Meta: ≥{BENCHMARK_CONVERSAO:.0%}",
        delta_color="normal",
    )
    c4.metric(
        "Taxa de Save",
        f"{kpis['taxa_save']:.1%}",
        delta=f"Meta: ≥{BENCHMARK_SAVE:.0%}",
        delta_color="normal",
    )
    c5.metric(
        "Retenção",
        f"{kpis['taxa_retencao']:.1%}",
        delta="2+ visitas",
        delta_color="normal",
    )

    st.divider()

    # ── Funil de engajamento ────────────────────────────────────────
    st.subheader("Funil de Engajamento")
    if kpis["total_views"] > 0:
        fig_funil = go.Figure(go.Funnel(
            y=["Visualizações", "Saves", "Compartilhamentos", "Check-ins"],
            x=[kpis["total_views"], kpis["total_saves"], kpis["total_shares"], kpis["total_checkins"]],
            textinfo="value+percent initial",
            marker=dict(color=[COR_PRIMARIA, COR_SECUNDARIA, COR_NEUTRO, COR_VERDE]),
        ))
        fig_funil.update_layout(
            title="Do interesse ao check-in",
            plot_bgcolor=COR_FUNDO,
            paper_bgcolor=COR_FUNDO,
            font=dict(color=COR_TEXTO),
        )
        st.plotly_chart(fig_funil, use_container_width=True, theme=None)
        st.markdown(
            '<div class="insight-box"><strong>Insight:</strong> '
            "Usuários que salvam o perfil têm 29% mais chance de fazer check-in. "
            "Incentive o 'Salvar' com chamadas visuais no seu perfil.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("Dados insuficientes para exibir o funil.")

    st.divider()

    # ── Status dos KPIs vs benchmarks ──────────────────────────────
    st.subheader("Status vs Metas da Plataforma")
    df_metas = pd.DataFrame({
        "KPI": ["Conversão", "Save", "Compartilhamento", "Uso de Promoção"],
        "Restaurantes": [
            kpis["taxa_conversao"],
            kpis["taxa_save"],
            kpis["taxa_compartilhar"],
            kpis["taxa_uso_promo"],
        ],
        "Meta Explori": [
            BENCHMARK_CONVERSAO,
            BENCHMARK_SAVE,
            BENCHMARK_COMPARTILHAR,
            BENCHMARK_USO_PROMO,
        ],
    })
    fig_metas = px.bar(
        df_metas.melt(id_vars="KPI", var_name="Tipo", value_name="Taxa"),
        x="KPI",
        y="Taxa",
        color="Tipo",
        barmode="group",
        color_discrete_map={"Restaurantes": COR_PRIMARIA, "Meta Explori": COR_NEUTRO},
        text_auto=".1%",
        title="Comparativo:Restaurantes vs Metas da Plataforma",
        labels={"Taxa": "Taxa (%)", "KPI": "Indicador"},
    )
    fig_metas.update_layout(
        plot_bgcolor=COR_FUNDO,
        paper_bgcolor=COR_FUNDO,
        font=dict(color=COR_TEXTO),
        yaxis=dict(tickformat=".0%"),
    )
    st.plotly_chart(fig_metas, use_container_width=True)

    st.divider()
