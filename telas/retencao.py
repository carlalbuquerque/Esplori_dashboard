import plotly.express as px
import streamlit as st

from utils.constantes import COR_FUNDO, COR_PRIMARIA, COR_TEXTO, COR_VERDE


def render(dados: tuple, kpis: dict) -> None:
    usuarios, _e, _c, _ec, checkins, _i, _p = dados
    retencao = kpis["retencao"]

    st.title("Retenção de Clientes")
    st.caption("Quantos clientes voltam após a primeira visita ao seu restaurante?")

    if retencao.empty:
        st.warning("Dados de check-in insuficientes para calcular retenção.")
        return

    # ── KPIs de retenção ─────────────────────────────────────────────
    total_usuarios_checkin = len(retencao)
    usuarios_1      = int((retencao["num_checkins"] == 1).sum())
    usuarios_2_mais = int((retencao["num_checkins"] >= 2).sum())
    usuarios_3_mais = int((retencao["num_checkins"] >= 3).sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de Visitantes", f"{total_usuarios_checkin:,}")
    c2.metric(
        "Visita Única",
        f"{usuarios_1 / total_usuarios_checkin:.1%}",
        delta="~84% na plataforma",
        delta_color="off",
    )
    c3.metric(
        "Recorrentes (2+)",
        f"{usuarios_2_mais / total_usuarios_checkin:.1%}",
        delta="Voltaram",
        delta_color="normal",
    )
    c4.metric(
        "Fiéis (3+)",
        f"{usuarios_3_mais / total_usuarios_checkin:.1%}",
        delta="~1,66% na plataforma",
        delta_color="off",
    )

    st.divider()

    # ── Distribuição de check-ins por usuário ────────────────────────
    st.subheader("Distribuição de Check-ins por Usuário")
    df_dist = retencao["num_checkins"].clip(upper=5).value_counts().sort_index().reset_index()
    df_dist.columns = ["Check-ins", "Usuários"]
    df_dist["Check-ins"] = df_dist["Check-ins"].astype(str)
    df_dist.loc[df_dist["Check-ins"] == "5", "Check-ins"] = "5+"

    if not df_dist.empty:
        fig_dist = px.bar(
            df_dist,
            x="Check-ins",
            y="Usuários",
            color_discrete_sequence=[COR_PRIMARIA],
            text="Usuários",
            title="Quantas vezes cada usuário visitou",
            labels={"Check-ins": "Número de Check-ins", "Usuários": "Quantidade de Usuários"},
        )
        fig_dist.update_traces(textposition="outside")
        fig_dist.update_layout(
            plot_bgcolor=COR_FUNDO,
            paper_bgcolor=COR_FUNDO,
            font=dict(color=COR_TEXTO),
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        st.markdown(
            '<div class="insight-box"><strong>Insight:</strong> '
            "84% dos usuários fazem apenas 1 check-in. Criar uma oferta exclusiva para a segunda visita "
            "é o maior alavancador de receita disponível — transforme visitantes únicos em recorrentes.</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Retenção por faixa etária ────────────────────────────────────
    if not checkins.empty and not usuarios.empty and "faixa_etaria" in usuarios.columns:
        st.subheader("Taxa de Retenção por Faixa Etária")
        df_ret_faixa = (
            checkins.merge(
                usuarios[["id_usuario", "faixa_etaria"]],
                on="id_usuario",
                how="left",
            )
            .groupby(["id_usuario", "faixa_etaria"], observed=False)
            .size()
            .reset_index(name="num_checkins")
        )
        df_ret_faixa_agg = (
            df_ret_faixa.groupby("faixa_etaria", observed=False)
            .apply(lambda g: (g["num_checkins"] >= 2).sum() / len(g), include_groups=False)
            .reset_index(name="taxa_retencao")
        )
        df_ret_faixa_agg["taxa_retencao_fmt"] = df_ret_faixa_agg["taxa_retencao"].map(
            lambda x: f"{x:.1%}"
        )

        if not df_ret_faixa_agg.empty:
            fig_ret_faixa = px.bar(
                df_ret_faixa_agg,
                x="faixa_etaria",
                y="taxa_retencao",
                color_discrete_sequence=[COR_VERDE],
                text="taxa_retencao_fmt",
                title="Taxa de Retenção (2+ visitas) por Faixa Etária",
                labels={
                    "faixa_etaria": "Faixa Etária",
                    "taxa_retencao": "Taxa de Retenção",
                },
            )
            fig_ret_faixa.update_traces(textposition="outside")
            fig_ret_faixa.update_layout(
                plot_bgcolor=COR_FUNDO,
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
                yaxis=dict(tickformat=".0%"),
            )
            st.plotly_chart(fig_ret_faixa, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "Identifique qual faixa etária tem maior tendência de retorno e direcione "
                "campanhas de fidelização especificamente para esse público.</div>",
                unsafe_allow_html=True,
            )

    st.divider()
