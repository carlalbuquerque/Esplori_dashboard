import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.constantes import (
    BENCHMARK_COMPARTILHAR,
    BENCHMARK_CONVERSAO,
    BENCHMARK_RETENCAO,
    BENCHMARK_SAVE,
    BENCHMARK_USO_PROMO,
    COR_FUNDO,
    COR_NEUTRO,
    COR_PRIMARIA,
    COR_SECUNDARIA,
    COR_TEXTO,
)


def render(dados: tuple, kpis: dict) -> None:
    _u, estab, _c, _ec, _ch, _i, _p = dados

    st.title("Benchmarking")
    st.caption("Compare o desempenho do seu restaurante com os benchmarks da plataforma Explori.")

    # ── Radar de performance ─────────────────────────────────────────
    st.subheader("Posicionamento vs Metas da Plataforma")
    categorias_radar = ["Conversão", "Save", "Compartilhamento", "Uso de Promoção", "Retenção"]
    valores_restaurante = [
        min(kpis["taxa_conversao"]    / BENCHMARK_CONVERSAO,    2.0),
        min(kpis["taxa_save"]         / BENCHMARK_SAVE,         2.0),
        min(kpis["taxa_compartilhar"] / BENCHMARK_COMPARTILHAR, 2.0),
        min(kpis["taxa_uso_promo"]    / BENCHMARK_USO_PROMO,    2.0),
        min(kpis["taxa_retencao"]     / BENCHMARK_RETENCAO,     2.0),
    ]
    valores_meta = [1.0, 1.0, 1.0, 1.0, 1.0]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=valores_restaurante + [valores_restaurante[0]],
        theta=categorias_radar + [categorias_radar[0]],
        fill="toself",
        fillcolor="rgba(224,122,47,0.2)",
        line=dict(color=COR_PRIMARIA, width=2),
        name="Seu Restaurante",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=valores_meta + [valores_meta[0]],
        theta=categorias_radar + [categorias_radar[0]],
        fill="toself",
        fillcolor="rgba(138,148,80,0.1)",
        line=dict(color=COR_NEUTRO, width=2, dash="dash"),
        name="Meta Explori",
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 2.0], tickformat=".0%"),
        ),
        paper_bgcolor=COR_FUNDO,
        font=dict(color=COR_TEXTO),
        title="Performance relativa às metas (1.0 = meta atingida)",
        showlegend=True,
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown(
        '<div class="insight-box"><strong>Insight:</strong> '
        "Valores acima de 1.0 indicam que você superou a meta. "
        "Foque nos indicadores abaixo de 1.0 para crescimento prioritário.</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Tabela comparativa detalhada ────────────────────────────────
    st.subheader("Comparativo Detalhado")
    df_comp = pd.DataFrame({
        "Indicador": [
            "Taxa de Conversão",
            "Taxa de Save",
            "Compartilhamentos",
            "Uso de Promoção",
            "Retenção (2+)",
        ],
        "Seu Restaurante": [
            f"{kpis['taxa_conversao']:.1%}",
            f"{kpis['taxa_save']:.1%}",
            f"{kpis['taxa_compartilhar']:.1%}",
            f"{kpis['taxa_uso_promo']:.1%}",
            f"{kpis['taxa_retencao']:.1%}",
        ],
        "Meta Explori": [
            f"≥{BENCHMARK_CONVERSAO:.0%}",
            f"≥{BENCHMARK_SAVE:.0%}",
            f"≥{BENCHMARK_COMPARTILHAR:.0%}",
            f"≥{BENCHMARK_USO_PROMO:.0%}",
            f">{BENCHMARK_RETENCAO:.0%}",
        ],
        "Status": [
            "OK" if kpis["taxa_conversao"]    >= BENCHMARK_CONVERSAO    else "Alerta",
            "OK" if kpis["taxa_save"]         >= BENCHMARK_SAVE         else "Alerta",
            "OK" if kpis["taxa_compartilhar"] >= BENCHMARK_COMPARTILHAR else "Alerta",
            "OK" if kpis["taxa_uso_promo"]    >= BENCHMARK_USO_PROMO    else "Alerta",
            "OK" if kpis["taxa_retencao"]     >= BENCHMARK_RETENCAO     else "Alerta",
        ],
    })
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

    st.divider()

    # ── Distribuição por faixa de gasto (concorrência) ───────────────
    if not estab.empty and "faixa_de_gasto" in estab.columns:
        st.subheader("Distribuição de Restaurantes por Faixa de Gasto")
        df_faixa_estab = estab["faixa_de_gasto"].value_counts().reset_index()
        df_faixa_estab.columns = ["Faixa de Gasto", "Restaurantes"]
        if not df_faixa_estab.empty:
            fig_faixa_estab = px.bar(
                df_faixa_estab,
                x="Faixa de Gasto",
                y="Restaurantes",
                color_discrete_sequence=[COR_PRIMARIA, COR_SECUNDARIA, COR_NEUTRO],
                text="Restaurantes",
                title="Concorrência por Faixa de Gasto na Plataforma",
                labels={
                    "Faixa de Gasto": "Faixa de Gasto",
                    "Restaurantes": "Nº de Restaurantes",
                },
            )
            fig_faixa_estab.update_traces(textposition="outside")
            fig_faixa_estab.update_layout(
                plot_bgcolor=COR_FUNDO,
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
            )
            st.plotly_chart(fig_faixa_estab, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "A faixa 'baixo' domina em volume de restaurantes. Estabelecimentos de ticket "
                "médio e alto têm menos concorrência direta — use isso como diferencial.</div>",
                unsafe_allow_html=True,
            )

    st.divider()
