import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.constantes import (
    BENCHMARK_COMPARTILHAR,
    BENCHMARK_CONVERSAO,
    BENCHMARK_SAVE,
    COR_FUNDO,
    COR_NEUTRO,
    COR_PRIMARIA,
    COR_SECUNDARIA,
    COR_TEXTO,
    COR_VERDE,
)


def render(dados: tuple, kpis: dict) -> None:
    _u, estab, _c, _ec, _ch, interacoes, _p = dados

    st.title("Engajamento")
    st.caption("Funil completo de engajamento: da visualização ao check-in.")

    # ── KPIs de engajamento ─────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Visualizações", f"{kpis['total_views']:,}")
    c2.metric(
        "Taxa de Conversão",
        f"{kpis['taxa_conversao']:.1%}",
        delta=f"Meta ≥{BENCHMARK_CONVERSAO:.0%}",
        delta_color="normal",
    )
    c3.metric(
        "Taxa de Save",
        f"{kpis['taxa_save']:.1%}",
        delta=f"Meta ≥{BENCHMARK_SAVE:.0%}",
        delta_color="normal",
    )
    c4.metric(
        "Compartilhamentos",
        f"{kpis['taxa_compartilhar']:.1%}",
        delta=f"Meta ≥{BENCHMARK_COMPARTILHAR:.0%}",
        delta_color="normal",
    )

    st.divider()

    # ── Funil detalhado ─────────────────────────────────────────────
    st.subheader("Funil de Engajamento — Detalhado")
    if kpis["total_views"] > 0:
        fig_funil = go.Figure(go.Funnel(
            y=["Visualizações", "Saves", "Compartilhamentos", "Check-ins"],
            x=[kpis["total_views"], kpis["total_saves"], kpis["total_shares"], kpis["total_checkins"]],
            textinfo="value+percent initial",
            marker=dict(color=[COR_PRIMARIA, COR_SECUNDARIA, COR_NEUTRO, COR_VERDE]),
        ))
        fig_funil.update_layout(
            title="Funil completo — visualizações até check-in",
            paper_bgcolor=COR_FUNDO,
            font=dict(color=COR_TEXTO),
        )
        st.plotly_chart(fig_funil, use_container_width=True)
        st.markdown(
            '<div class="insight-box"><strong>Insight:</strong> '
            "Cada etapa do funil representa uma decisão do usuário. "
            "O maior drop-off costuma ocorrer entre visualizações e saves — "
            "melhore as fotos e descrição do perfil para aumentar a taxa de save.</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Engajamento por faixa de gasto ──────────────────────────────
    if not interacoes.empty and not estab.empty:
        st.subheader("Engajamento por Faixa de Gasto")
        df_eng = interacoes.merge(
            estab[["id_estabelecimento", "faixa_de_gasto"]],
            on="id_estabelecimento",
            how="left",
        )
        if not df_eng.empty and "faixa_de_gasto" in df_eng.columns:
            df_faixa_gasto = (
                df_eng.groupby("faixa_de_gasto", observed=False)[
                    ["visualizacoes_perfil", "saves_favoritos", "compartilhamentos"]
                ]
                .mean()
                .round(2)
                .reset_index()
            )
            df_faixa_gasto_melt = df_faixa_gasto.melt(
                id_vars="faixa_de_gasto",
                var_name="Métrica",
                value_name="Média",
            )
            mapa_metricas = {
                "visualizacoes_perfil": "Visualizações",
                "saves_favoritos": "Saves",
                "compartilhamentos": "Compartilhamentos",
            }
            df_faixa_gasto_melt["Métrica"] = df_faixa_gasto_melt["Métrica"].map(mapa_metricas)

            if not df_faixa_gasto_melt.empty:
                fig_faixa = px.bar(
                    df_faixa_gasto_melt,
                    x="faixa_de_gasto",
                    y="Média",
                    color="Métrica",
                    barmode="group",
                    color_discrete_map={
                        "Visualizações": COR_PRIMARIA,
                        "Saves": COR_VERDE,
                        "Compartilhamentos": COR_SECUNDARIA,
                    },
                    title="Engajamento Médio por Faixa de Gasto",
                    labels={
                        "faixa_de_gasto": "Faixa de Gasto",
                        "Média": "Média por Estabelecimento",
                    },
                )
                fig_faixa.update_layout(
                    plot_bgcolor=COR_FUNDO,
                    paper_bgcolor=COR_FUNDO,
                    font=dict(color=COR_TEXTO),
                )
                st.plotly_chart(fig_faixa, use_container_width=True)
                st.markdown(
                    '<div class="insight-box"><strong>Insight:</strong> '
                    "A faixa de gasto 'baixo' domina em volume. Restaurantes de ticket alto "
                    "devem apostar em experiência diferenciada para aumentar conversão.</div>",
                    unsafe_allow_html=True,
                )

    st.divider()
