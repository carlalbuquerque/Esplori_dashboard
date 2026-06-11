import plotly.express as px
import streamlit as st

from utils.constantes import COR_FUNDO, COR_NEUTRO, COR_PRIMARIA, COR_SECUNDARIA, COR_TEXTO, COR_VERDE


def render(dados: tuple, kpis: dict) -> None:
    _u, _e, _c, _ec, checkins, _i, promocoes = dados

    st.title("Desempenho de Promoções")
    st.caption("Acompanhe o aproveitamento das suas promoções e o impacto no engajamento.")

    if promocoes.empty:
        st.warning("Dados de promoções não disponíveis.")
        return

    # ── KPIs de promoções ────────────────────────────────────────────
    total_promos = len(promocoes)
    promo_alta   = int((promocoes["taxa_uso"] >= 0.70).sum()) if "taxa_uso" in promocoes.columns else 0
    promo_baixa  = int((promocoes["taxa_uso"] < 0.30).sum()) if "taxa_uso" in promocoes.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de Promoções", f"{total_promos:,}")
    c2.metric(
        "Uso Médio",
        f"{kpis['taxa_uso_promo']:.1%}",
        delta="Meta: ≥70%",
        delta_color="normal",
    )
    c3.metric("Alto Aproveitamento (>=70%)", f"{promo_alta}")
    c4.metric("Baixo Aproveitamento (<30%)", f"{promo_baixa}")

    st.divider()

    # ── Distribuição da taxa de uso ──────────────────────────────────
    st.subheader("Distribuição da Taxa de Uso das Promoções")
    if "taxa_uso" in promocoes.columns:
        fig_hist = px.histogram(
            promocoes,
            x="taxa_uso",
            nbins=20,
            color_discrete_sequence=[COR_PRIMARIA],
            title="Distribuição do Aproveitamento das Promoções",
            labels={"taxa_uso": "Taxa de Uso", "count": "Quantidade de Promoções"},
        )
        fig_hist.add_vline(x=0.70, line_dash="dash", line_color=COR_VERDE, annotation_text="Meta 70%")
        fig_hist.add_vline(x=0.30, line_dash="dash", line_color=COR_SECUNDARIA, annotation_text="Alerta 30%")
        fig_hist.update_layout(
            plot_bgcolor=COR_FUNDO,
            paper_bgcolor=COR_FUNDO,
            font=dict(color=COR_TEXTO),
            xaxis=dict(tickformat=".0%"),
            yaxis_title="Quantidade de Promoções",
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown(
            '<div class="insight-box"><strong>Insight:</strong> '
            "A maioria das promoções não atinge 100% de aproveitamento. "
            "Para promoções com uso abaixo de 30%, revise o prazo de validade, "
            "o valor do desconto e o canal de divulgação.</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Impacto do voucher nos check-ins ─────────────────────────────
    if not checkins.empty and "usou_voucher" in checkins.columns:
        st.subheader("Impacto do Voucher nos Check-ins")
        df_voucher = (
            checkins["usou_voucher"]
            .map({True: "Com Voucher", False: "Sem Voucher", 1: "Com Voucher", 0: "Sem Voucher"})
            .value_counts()
            .reset_index()
        )
        df_voucher.columns = ["Tipo", "Check-ins"]
        if not df_voucher.empty:
            fig_voucher = px.pie(
                df_voucher,
                names="Tipo",
                values="Check-ins",
                color_discrete_map={"Com Voucher": COR_VERDE, "Sem Voucher": COR_NEUTRO},
                hole=0.45,
                title="Check-ins com e sem Voucher",
            )
            fig_voucher.update_layout(
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
            )
            st.plotly_chart(fig_voucher, use_container_width=True)

    st.divider()

    # ── Promoções com baixo aproveitamento ───────────────────────────
    if "taxa_uso" in promocoes.columns:
        st.subheader("Promoções com Baixo Aproveitamento")
        colunas_exibir = [col for col in promocoes.columns if col not in ["id_promocao", "id_estabelecimento"]]
        df_baixo = (
            promocoes[promocoes["taxa_uso"] < 0.30][colunas_exibir]
            .sort_values("taxa_uso")
            .head(10)
        )
        if not df_baixo.empty:
            df_baixo = df_baixo.copy()
            df_baixo["taxa_uso"] = df_baixo["taxa_uso"].map(lambda x: f"{x:.1%}")
            st.dataframe(df_baixo, use_container_width=True)
        else:
            st.success("Nenhuma promoção com aproveitamento abaixo de 30%.")

    st.divider()
