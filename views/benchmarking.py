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
    COR_VERDE,
)


def render(dados: tuple, kpis: dict) -> None:
    _u, estab, categorias, estab_cat, checkins, _i, _p = dados

    st.title("Benchmarking")
    st.caption("Compare o desempenho de restaurantes com os benchmarks da plataforma Explori.")

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
        name="Restaurantes cadastrados",
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

    # ── Categorias em Alta e em Baixa ────────────────────────────────
    st.subheader("Categorias em Alta e em Baixa")

    if not categorias.empty and not checkins.empty:
        df_cat_ch = checkins.merge(categorias, on="id_categoria", how="left")

        if not df_cat_ch.empty and "nome_categoria" in df_cat_ch.columns:

            # ── Preparar coluna de mês ────────────────────────────────
            _MESES_PT = {
                "01": "Jan", "02": "Fev", "03": "Mar", "04": "Abr",
                "05": "Mai", "06": "Jun", "07": "Jul", "08": "Ago",
                "09": "Set", "10": "Out", "11": "Nov", "12": "Dez",
            }
            if "data_hora_checkin" in df_cat_ch.columns:
                df_cat_ch["_dt"] = pd.to_datetime(df_cat_ch["data_hora_checkin"], errors="coerce")
                df_cat_ch["mes"] = df_cat_ch["_dt"].dt.to_period("M").astype(str)
                df_cat_ch["mes_label"] = df_cat_ch["mes"].apply(
                    lambda m: f"{_MESES_PT.get(m[5:7], m[5:7])}/{m[2:4]}" if isinstance(m, str) and len(m) == 7 else m
                )
                meses_disponiveis = sorted(df_cat_ch["mes"].dropna().unique().tolist())
                mes_para_label = {
                    m: f"{_MESES_PT.get(m[5:7], m[5:7])}/{m[2:4]}" for m in meses_disponiveis
                }
                label_para_mes = {v: k for k, v in mes_para_label.items()}
                labels_disponiveis = [mes_para_label[m] for m in meses_disponiveis]
            else:
                meses_disponiveis = []
                labels_disponiveis = []
                mes_para_label = {}
                label_para_mes = {}

            # ── Filtros lado a lado ───────────────────────────────────
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                default_labels = labels_disponiveis[-6:] if len(labels_disponiveis) >= 6 else labels_disponiveis
                labels_sel = st.multiselect(
                    "Filtrar por mês",
                    options=labels_disponiveis,
                    default=default_labels,
                    placeholder="Selecione um ou mais meses",
                )
                meses_sel = [label_para_mes[lb] for lb in labels_sel if lb in label_para_mes]
            with col_f2:
                top_n = st.slider("Nº de categorias exibidas", min_value=3, max_value=20, value=10)

            df_filtrado = df_cat_ch[df_cat_ch["mes"].isin(meses_sel)] if meses_sel else df_cat_ch

            if df_filtrado.empty:
                st.info("Nenhum dado para o período selecionado.")
            else:
                # ── Ranking de categorias ─────────────────────────────
                df_volume = (
                    df_filtrado
                    .groupby("nome_categoria", observed=True)["id_checkin"]
                    .count()
                    .reset_index()
                    .rename(columns={"nome_categoria": "Categoria", "id_checkin": "Check-ins"})
                    .sort_values("Check-ins", ascending=False)
                    .head(top_n)
                    .reset_index(drop=True)
                )

                n = len(df_volume)
                cores = [COR_NEUTRO] * n
                top3 = min(3, n)
                bot3 = min(3, n)
                for i in range(top3):
                    cores[i] = COR_VERDE
                for i in range(n - bot3, n):
                    if cores[i] != COR_VERDE:
                        cores[i] = COR_SECUNDARIA

                # barras horizontais — categorias no eixo Y, sem problema de leitura
                df_volume_inv = df_volume.iloc[::-1].reset_index(drop=True)
                cores_inv = cores[::-1]

                fig_bar = go.Figure(go.Bar(
                    x=df_volume_inv["Check-ins"],
                    y=df_volume_inv["Categoria"],
                    orientation="h",
                    marker_color=cores_inv,
                    text=df_volume_inv["Check-ins"],
                    textposition="outside",
                    textfont=dict(color=COR_TEXTO, size=13),
                ))
                altura_bar = max(400, n * 48)
                fig_bar.update_traces(textfont=dict(color=COR_TEXTO, size=13))
                fig_bar.update_layout(
                    title=dict(text=f"Top {top_n} Categorias por Volume de Check-ins", font=dict(color=COR_TEXTO, size=16)),
                    xaxis=dict(
                        title="Nº de Check-ins",
                        tickfont=dict(color=COR_TEXTO, size=12),
                        title_font=dict(color=COR_TEXTO, size=14),
                    ),
                    yaxis=dict(
                        title="",
                        tickfont=dict(color=COR_TEXTO, size=13),
                        automargin=True,
                    ),
                    plot_bgcolor=COR_FUNDO,
                    paper_bgcolor=COR_FUNDO,
                    font=dict(color=COR_TEXTO, size=12),
                    height=altura_bar,
                    margin=dict(t=60, b=40, l=200, r=80),
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown(
                    '<div class="insight-box"> <strong>Insight:</strong> '
                    "Categorias em <strong>verde</strong> lideram (em alta). "
                    "As em <strong>laranja escuro</strong> têm menor engajamento — avalie ações para aquecê-las.</div>",
                    unsafe_allow_html=True,
                )

                # ── Heatmap top N por mês ─────────────────────────────
                if meses_sel:
                    cats_top = df_volume["Categoria"].tolist()
                    df_heat_src = df_filtrado[df_filtrado["nome_categoria"].isin(cats_top)].copy()
                    df_heat_src["mes_label"] = df_heat_src["mes"].map(mes_para_label)
                    # garante ordem cronológica dos labels selecionados
                    labels_sel_ord = [mes_para_label[m] for m in sorted(meses_sel) if m in mes_para_label]
                    df_heatmap = (
                        df_heat_src
                        .groupby(["nome_categoria", "mes_label"], observed=True)["id_checkin"]
                        .count()
                        .reset_index()
                        .rename(columns={"nome_categoria": "Categoria", "mes_label": "Mês", "id_checkin": "Check-ins"})
                    )
                    df_pivot = (
                        df_heatmap
                        .pivot(index="Categoria", columns="Mês", values="Check-ins")
                        .reindex(columns=labels_sel_ord)
                        .fillna(0)
                    )
                    # ordena linhas igual ao ranking de barras
                    df_pivot = df_pivot.reindex([c for c in df_volume["Categoria"] if c in df_pivot.index])

                    if not df_pivot.empty:
                        altura_heatmap = max(350, len(df_pivot) * 50)
                        fig_heat = go.Figure(go.Heatmap(
                            z=df_pivot.values.tolist(),
                            x=df_pivot.columns.tolist(),
                            y=df_pivot.index.tolist(),
                            colorscale=[
                                [0.0, "#F9F5F0"],
                                [0.4, "#E8C4A0"],
                                [0.7, "#B96A4A"],
                                [1.0, "#E07A2F"],
                            ],
                            texttemplate="%{z:.0f}",
                            textfont=dict(color=COR_TEXTO, size=13),
                            hovertemplate="Categoria: %{y}<br>Mês: %{x}<br>Check-ins: %{z}<extra></extra>",
                            showscale=True,
                            colorbar=dict(title="Check-ins", tickfont=dict(color=COR_TEXTO)),
                        ))
                        fig_heat.data[0].textfont = dict(color=COR_TEXTO, size=13)
                        fig_heat.update_layout(
                            title=dict(text=f"Tendência Mensal — Top {top_n} Categorias", font=dict(color=COR_TEXTO, size=16)),
                            xaxis=dict(
                                title="Mês",
                                tickangle=0,
                                tickfont=dict(color=COR_TEXTO, size=13),
                                title_font=dict(color=COR_TEXTO, size=14),
                                side="bottom",
                            ),
                            yaxis=dict(
                                title="",
                                tickfont=dict(color=COR_TEXTO, size=13),
                                autorange="reversed",
                            ),
                            plot_bgcolor=COR_FUNDO,
                            paper_bgcolor=COR_FUNDO,
                            font=dict(color=COR_TEXTO, size=13),
                            height=altura_heatmap,
                            margin=dict(t=70, b=80, l=210, r=100),
                        )
                        fig_heat.data[0].colorbar.tickfont = dict(color=COR_TEXTO)
                        st.plotly_chart(fig_heat, use_container_width=True)
                        st.markdown(
                            '<div class="insight-box"><strong>Insight:</strong> '
                            "Células mais escuras = maior concentração de check-ins no período. "
                            "Acompanhe quais categorias crescem mês a mês para antecipar tendências.</div>",
                            unsafe_allow_html=True,
                        )

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
                color_discrete_sequence=[COR_SECUNDARIA, COR_NEUTRO, COR_TEXTO],
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
                font=dict(color="#1A1A1A", size=14),
            )
            st.plotly_chart(fig_faixa_estab, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "A faixa 'baixo' domina em volume de restaurantes. Estabelecimentos de ticket "
                "médio e alto têm menos concorrência direta — use isso como diferencial.</div>",
                unsafe_allow_html=True,
            )

    st.divider()
