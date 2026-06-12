import plotly.express as px
import streamlit as st

from utils.constantes import COR_FUNDO, COR_NEUTRO, COR_PRIMARIA, COR_SECUNDARIA, COR_TEXTO, COR_VERDE


def render(dados: tuple, kpis: dict) -> None:
    _u, estab, _c, _ec, checkins, _i, promocoes = dados

    MESES_PT = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
    }

    st.title("Desempenho de Promoções")
    st.caption("Acompanhe o aproveitamento de promoções e o impacto no engajamento.")

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

    # ── Uso de voucher por mês ───────────────────────────────────────
    if not checkins.empty and "usou_voucher" in checkins.columns and "data_hora_checkin" in checkins.columns:
        st.subheader("Uso de Voucher por Mês")
        df_mes = checkins.copy()
        df_mes = df_mes.dropna(subset=["data_hora_checkin"])
        df_mes["mes_num"] = df_mes["data_hora_checkin"].dt.month
        df_mes["ano"] = df_mes["data_hora_checkin"].dt.year
        df_mes["usou_voucher"] = df_mes["usou_voucher"].map(
            {True: "Com Voucher", False: "Sem Voucher", 1: "Com Voucher", 0: "Sem Voucher"}
        ).fillna("Sem Voucher")
        df_mes_agg = (
            df_mes.groupby(["ano", "mes_num", "usou_voucher"])
            .size()
            .reset_index(name="Check-ins")
        )
        df_mes_agg["Mês"] = df_mes_agg["mes_num"].map(MESES_PT) + "/" + df_mes_agg["ano"].astype(str).str[-2:]
        df_mes_agg = df_mes_agg.sort_values(["ano", "mes_num"])
        if not df_mes_agg.empty:
            fig_mes = px.line(
                df_mes_agg,
                x="Mês",
                y="Check-ins",
                color="usou_voucher",
                markers=True,
                color_discrete_map={"Com Voucher": COR_VERDE, "Sem Voucher": COR_SECUNDARIA},
                title="Check-ins com e sem Voucher por Mês",
                labels={"usou_voucher": "Tipo", "Check-ins": "Quantidade de Check-ins", "Mês": "Mês"},
            )
            fig_mes.update_layout(
                plot_bgcolor=COR_FUNDO,
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
            )
            st.plotly_chart(fig_mes, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "Meses com maior uso de voucher indicam campanhas mais efetivas. "
                "Compare os picos com as datas em que promoções foram lançadas para "
                "identificar o melhor período para divulgação.</div>",
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
                color="Tipo",
                color_discrete_map={"Com Voucher": COR_VERDE, "Sem Voucher": COR_SECUNDARIA},
                hole=0.45,
                title="Check-ins com e sem Voucher",
            )
            fig_voucher.update_traces(textinfo="percent+value", textposition="outside")
            fig_voucher.update_layout(
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
            )
            st.plotly_chart(fig_voucher, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "Usuários que utilizam voucher têm maior probabilidade de completar o check-in. "
                "Promova vouchers nos horários de pico para aumentar a taxa de conversão.</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Promoções com baixo aproveitamento ───────────────────────────
    if "taxa_uso" in promocoes.columns:
        st.subheader("Promoções com Baixo Aproveitamento")
        df_baixo = (
            promocoes[promocoes["taxa_uso"] < 0.30]
            .sort_values("taxa_uso")
            .head(10)
            .copy()
        )
        if not df_baixo.empty:
            if not estab.empty and "nome_estabelecimento" in estab.columns:
                df_baixo = df_baixo.merge(
                    estab[["id_estabelecimento", "nome_estabelecimento"]],
                    on="id_estabelecimento",
                    how="left",
                )
                df_baixo["Promoção"] = df_baixo["nome_estabelecimento"].fillna(
                    "Promo #" + df_baixo["id_promocao"].astype(int).astype(str)
                )
            else:
                df_baixo["Promoção"] = "Promo #" + df_baixo["id_promocao"].astype(int).astype(str)
            df_baixo["Taxa de Uso (%)"] = (df_baixo["taxa_uso"] * 100).round(1)
            fig_baixo = px.bar(
                df_baixo.sort_values("Taxa de Uso (%)"),
                x="Taxa de Uso (%)",
                y="Promoção",
                orientation="h",
                color_discrete_sequence=[COR_SECUNDARIA],
                text="Taxa de Uso (%)",
                title="Top 10 Promoções com Menor Aproveitamento (< 30%)",
                labels={"Taxa de Uso (%)": "Taxa de Uso (%)", "Promoção": ""},
            )
            fig_baixo.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                textfont=dict(color=COR_TEXTO),
            )
            fig_baixo.add_vline(x=30, line_dash="dash", line_color=COR_PRIMARIA, annotation_text="Limite 30%")
            fig_baixo.update_layout(
                plot_bgcolor=COR_FUNDO,
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
                xaxis=dict(range=[0, 40], tickfont=dict(color=COR_TEXTO)),
                yaxis=dict(tickfont=dict(color=COR_TEXTO)),
            )
            st.plotly_chart(fig_baixo, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "Promoções abaixo de 30% de uso precisam de atenção. "
                "Revise o prazo de validade, o valor do desconto e o canal de divulgação.</div>",
                unsafe_allow_html=True,
            )
        else:
            st.success("Nenhuma promoção com aproveitamento abaixo de 30%.")

    st.divider()
