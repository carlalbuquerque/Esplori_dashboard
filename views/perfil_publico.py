import plotly.express as px
import streamlit as st

from utils.constantes import COR_FUNDO, COR_NEUTRO, COR_PRIMARIA, COR_SECUNDARIA, COR_TEXTO


def render(dados: tuple, kpis: dict) -> None:
    usuarios, _e, _c, _ec, _ch, _i, _p = dados

    # ── Normalização defensiva (independente do cache) ───────────────
    if not usuarios.empty and "genero" in usuarios.columns:
        usuarios = usuarios.copy()
        usuarios["genero"] = usuarios["genero"].str.replace(
            r"n[aã]o[\s_]+informado", "não informado", regex=True
        )

    st.title("Perfil do Público")
    st.caption("Entenda quem são os usuários que visualizam e visitam plataforma esplori.")

    if usuarios.empty:
        st.warning("Dados de usuários não disponíveis.")
        return

    col1, col2 = st.columns(2)

    # ── Faixa etária ────────────────────────────────────────────────
    with col1:
        st.subheader("Distribuição por Faixa Etária")
        df_faixa = (
            usuarios.groupby(["faixa_etaria", "genero"], observed=False)
            .size()
            .reset_index(name="Usuários")
            .rename(columns={"faixa_etaria": "Faixa Etária", "genero": "Gênero"})
            .sort_values("Faixa Etária")
        )
        if not df_faixa.empty:
            fig_faixa = px.bar(
                df_faixa,
                x="Faixa Etária",
                y="Usuários",
                color="Gênero",
                barmode="group",
                category_orders={
                    "Faixa Etária": ["18-25", "26-35", "36-45", "46-55", "56-65"],
                    "Gênero": ["feminino", "masculino", "não informado"],
                },
                color_discrete_map={
                    "masculino": COR_PRIMARIA,
                    "feminino": COR_SECUNDARIA,
                    "não informado": COR_NEUTRO,
                },
                text="Usuários",
                title="Faixa Etária dos Usuários por Gênero",
                labels={"Faixa Etária": "Faixa Etária", "Usuários": "Quantidade"},
            )
            fig_faixa.update_traces(textposition="outside")
            fig_faixa.update_layout(
                plot_bgcolor=COR_FUNDO,
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
            )
            st.plotly_chart(fig_faixa, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "As faixas 26-35 e 36-45 concentram o maior volume de usuários ativos. "
                "Crie promoções voltadas a experiências e descobertas para este público.</div>",
                unsafe_allow_html=True,
            )

    # ── Gênero ──────────────────────────────────────────────────────
    with col2:
        st.subheader("Distribuição por Gênero")
        df_genero = usuarios["genero"].value_counts().reset_index()
        df_genero.columns = ["Gênero", "Usuários"]
        if not df_genero.empty:
            fig_genero = px.pie(
                df_genero,
                names="Gênero",
                values="Usuários",
                color="Gênero",
                color_discrete_map={
                    "masculino": COR_PRIMARIA,
                    "feminino": COR_SECUNDARIA,
                    "não informado": COR_NEUTRO,
                },
                hole=0.45,
                title="Gênero dos Usuários",
            )
            fig_genero.update_layout(
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
            )
            st.plotly_chart(fig_genero, use_container_width=True)

    st.divider()

    # ── Origem geográfica ────────────────────────────────────────────
    st.subheader("Top 10 Cidades de Origem dos usuarios da plataforma esplori")
    df_cidades = (
        usuarios["origem_geografica"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    df_cidades.columns = ["Cidade", "Usuários"]
    df_cidades["Cidade"] = df_cidades["Cidade"].str.title()
    if not df_cidades.empty:
        fig_cidades = px.bar(
            df_cidades.sort_values("Usuários"),
            x="Usuários",
            y="Cidade",
            orientation="h",
            color_discrete_sequence=[COR_PRIMARIA],
            text="Usuários",
            title="Cidades de Origem — Top 10",
            labels={"Usuários": "Quantidade", "Cidade": ""},
        )
        fig_cidades.update_traces(textposition="outside")
        fig_cidades.update_layout(
            plot_bgcolor=COR_FUNDO,
            paper_bgcolor=COR_FUNDO,
            font=dict(color=COR_TEXTO),
            yaxis=dict(tickfont=dict(color=COR_TEXTO), autorange="reversed"),
        )
        st.plotly_chart(fig_cidades, use_container_width=True)
        st.markdown(
            '<div class="insight-box"><strong>Insight:</strong> '
            "Recife concentra ~46% dos usuários da plataforma. "
            "Campanhas segmentadas para a Região Metropolitana têm maior alcance e retorno.</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Top 10 Bairros ───────────────────────────────────────────────
    if "bairro" in usuarios.columns and "origem_geografica" in usuarios.columns:
        st.subheader("Top 10 Bairros dos usuarios da plataforma esplori")

        cidades = sorted(usuarios["origem_geografica"].dropna().str.title().unique())
        cidade_sel = st.selectbox(
            "Filtrar por cidade",
            options=["Todas"] + cidades,
            key="filtro_cidade_bairro",
        )

        df_bairros = usuarios.copy()
        df_bairros["origem_geografica"] = df_bairros["origem_geografica"].str.title()
        if cidade_sel != "Todas":
            df_bairros = df_bairros[df_bairros["origem_geografica"] == cidade_sel]

        df_bairros = (
            df_bairros["bairro"]
            .dropna()
            .str.title()
            .value_counts()
            .head(10)
            .reset_index()
        )
        df_bairros.columns = ["Bairro", "Usuários"]

        if not df_bairros.empty:
            fig_bairros = px.bar(
                df_bairros.sort_values("Usuários"),
                x="Usuários",
                y="Bairro",
                orientation="h",
                color_discrete_sequence=[COR_PRIMARIA],
                text="Usuários",
                title=f"Top 10 Bairros — {cidade_sel}",
                labels={"Usuários": "Quantidade", "Bairro": ""},
            )
            fig_bairros.update_traces(textposition="outside")
            fig_bairros.update_layout(
                plot_bgcolor=COR_FUNDO,
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
                yaxis=dict(tickfont=dict(color=COR_TEXTO), autorange="reversed"),
            )
            st.plotly_chart(fig_bairros, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "Concentre ações de marketing nos bairros com maior volume de usuários "
                "para maximizar o alcance das suas promoções.</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Horário de maior busca ───────────────────────────────────────
    if "hora" in usuarios.columns:
        st.subheader("Horário de Maior Atividade")
        df_hora = (
            usuarios["hora"]
            .dropna()
            .astype(int)
            .value_counts()
            .sort_index()
            .reset_index()
        )
        df_hora.columns = ["Hora", "Usuários"]
        if not df_hora.empty:
            fig_hora = px.bar(
                df_hora,
                x="Hora",
                y="Usuários",
                color_discrete_sequence=[COR_PRIMARIA],
                text="Usuários",
                title="Distribuição de Buscas por Hora do Dia",
                labels={"Hora": "Hora do Dia", "Usuários": "Quantidade de Buscas"},
            )
            fig_hora.update_traces(textposition="outside")
            fig_hora.update_layout(
                plot_bgcolor=COR_FUNDO,
                paper_bgcolor=COR_FUNDO,
                font=dict(color=COR_TEXTO),
                xaxis=dict(dtick=1),
            )
            st.plotly_chart(fig_hora, use_container_width=True)
            st.markdown(
                '<div class="insight-box"><strong>Insight:</strong> '
                "O pico de buscas ocorre entre 13h e 16h, com maior concentração às 14h. "
                "Publique promoções às 12h30 para capturar o público no momento de maior intenção.</div>",
                unsafe_allow_html=True,
            )

    st.divider()
