# ─── Carga e Limpeza de Dados ─────────────────────────────────────────────────
import os
import zipfile

import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados():
    """
    Carrega e trata todos os CSVs do dataset Explori.
    Ordem: EXTRACT → CLEAN → VALIDATE → DERIVE → RETURN
    Retorna tupla: (usuarios, estab, categorias, estab_cat, checkins, interacoes, promocoes)
    """
    base_dir    = os.path.dirname(os.path.abspath(__file__))
    data_dir    = os.path.normpath(os.path.join(base_dir, "..", "data"))
    extract_dir = os.path.join(data_dir, "extracted")

    # ── 1. Localizar ZIP ────────────────────────────────────────────
    zip_path = next(
        (os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".zip")),
        None,
    )

    # ── 2. Extrair com proteção path traversal ──────────────────────
    if zip_path and not os.path.exists(extract_dir):
        with zipfile.ZipFile(zip_path, "r") as z:
            for member in z.namelist():
                member_path = os.path.realpath(os.path.join(extract_dir, member))
                if not member_path.startswith(os.path.realpath(extract_dir)):
                    raise ValueError(f"Path traversal detectado no ZIP: {member}")
            z.extractall(extract_dir)

    # ── 3. Helper de leitura recursiva ──────────────────────────────
    csv_dir = extract_dir if os.path.exists(extract_dir) else data_dir

    def _read(name: str) -> pd.DataFrame:
        for root, _, files in os.walk(csv_dir):
            for fn in files:
                if fn == name:
                    df = pd.read_csv(os.path.join(root, fn))
                    # remove aspas simples/duplas que alguns CSVs incluem nos cabeçalhos
                    df.columns = df.columns.str.strip("'\"").str.strip()
                    return df
        return pd.DataFrame()

    # ── 4. Carregar tabelas ─────────────────────────────────────────
    usuarios   = _read("usuarios.csv")
    estab      = _read("estabelecimentos.csv")
    categorias = _read("categorias.csv")
    estab_cat  = _read("estabelecimento_categoria.csv")
    checkins   = _read("checkins.csv")
    interacoes = _read("interacoes.csv")
    promocoes  = _read("promocoes.csv")

    # ── 5. Tratar USUARIOS ──────────────────────────────────────────
    if not usuarios.empty:
        if "origem_geografica" in usuarios.columns:
            usuarios["origem_geografica"] = (
                usuarios["origem_geografica"].str.lower().str.strip()
            )
        usuarios["genero"] = (
            usuarios["genero"]
            .fillna("não informado")
            .str.lower()
            .str.strip()
            .str.replace("_", " ", regex=False)
            .str.replace(r"n[aã]o\s+informado", "não informado", regex=True)
        )
        usuarios["efetuou_checkin"] = usuarios["efetuou_checkin"].fillna(False).astype(bool)
        if "origem_geografica" in usuarios.columns:
            moda = usuarios["origem_geografica"].mode()
            if not moda.empty:
                usuarios["origem_geografica"] = usuarios["origem_geografica"].fillna(moda[0])
        usuarios.dropna(subset=["idade"], inplace=True)
        usuarios["idade"] = usuarios["idade"].astype(int)
        usuarios = usuarios[(usuarios["idade"] >= 18) & (usuarios["idade"] <= 65)].copy()
        usuarios.drop_duplicates(inplace=True)
        usuarios["faixa_etaria"] = pd.cut(
            usuarios["idade"],
            bins=[18, 25, 35, 45, 55, 65],
            labels=["18-25", "26-35", "36-45", "46-55", "56-65"],
            include_lowest=True,
        )
        if "horario_maior_busca" in usuarios.columns:
            usuarios["horario_maior_busca"] = pd.to_datetime(
                usuarios["horario_maior_busca"], format="%H:%M:%S", errors="coerce"
            )
            usuarios["hora"] = usuarios["horario_maior_busca"].dt.hour

    # ── 6. Tratar ESTABELECIMENTOS ──────────────────────────────────
    if not estab.empty:
        if "origem_geografica" in estab.columns:
            estab["origem_geografica"] = estab["origem_geografica"].str.lower().str.strip()
        estab["criacao_promocoes"] = estab["criacao_promocoes"].fillna(0)
        estab.drop_duplicates(inplace=True)

    # ── 7. Tratar CHECKINS ──────────────────────────────────────────
    if not checkins.empty:
        if "data_hora_checkin" in checkins.columns:
            checkins["data_hora_checkin"] = pd.to_datetime(
                checkins["data_hora_checkin"], errors="coerce"
            )
        checkins.dropna(inplace=True)
        checkins.drop_duplicates(inplace=True)

    # ── 8. Tratar INTERAÇÕES ────────────────────────────────────────
    if not interacoes.empty:
        for col in ["visualizacoes_perfil", "saves_favoritos", "compartilhamentos"]:
            if col in interacoes.columns:
                interacoes[col] = interacoes[col].fillna(0).astype(int)
        interacoes.drop_duplicates(inplace=True)

    # ── 9. Tratar PROMOÇÕES ─────────────────────────────────────────
    if not promocoes.empty:
        if "quantidade_disponibilizada" in promocoes.columns:
            mediana = promocoes["quantidade_disponibilizada"].median()
            promocoes["quantidade_disponibilizada"] = (
                promocoes["quantidade_disponibilizada"].fillna(mediana)
            )
        if (
            "quantidade_utilizada" in promocoes.columns
            and "quantidade_disponibilizada" in promocoes.columns
        ):
            promocoes["quantidade_utilizada"] = promocoes[
                ["quantidade_utilizada", "quantidade_disponibilizada"]
            ].min(axis=1)
            promocoes["taxa_uso"] = (
                promocoes["quantidade_utilizada"] / promocoes["quantidade_disponibilizada"]
            )
        promocoes.drop_duplicates(inplace=True)

    return usuarios, estab, categorias, estab_cat, checkins, interacoes, promocoes


def calcular_kpis(checkins, interacoes, promocoes):
    """
    Calcula os KPIs globais a partir dos dados já limpos.
    Retorna dicionário com todas as métricas usadas pelas telas.
    """
    total_views    = int(interacoes["visualizacoes_perfil"].sum()) if not interacoes.empty else 0
    total_saves    = int(interacoes["saves_favoritos"].sum()) if not interacoes.empty else 0
    total_shares   = int(interacoes["compartilhamentos"].sum()) if not interacoes.empty else 0
    total_checkins = len(checkins) if not checkins.empty else 0

    taxa_conversao    = total_checkins / total_views if total_views > 0 else 0.0
    taxa_save         = total_saves / total_views if total_views > 0 else 0.0
    taxa_compartilhar = total_shares / total_views if total_views > 0 else 0.0

    retencao = pd.DataFrame()
    taxa_retencao = 0.0
    if not checkins.empty and "id_usuario" in checkins.columns:
        retencao = checkins.groupby("id_usuario").size().reset_index(name="num_checkins")
        taxa_retencao = (
            (retencao["num_checkins"] >= 2).sum() / len(retencao)
            if len(retencao) > 0 else 0.0
        )

    taxa_uso_promo = 0.0
    if not promocoes.empty and "taxa_uso" in promocoes.columns:
        taxa_uso_promo = float(promocoes["taxa_uso"].mean())

    return {
        "total_views":       total_views,
        "total_saves":       total_saves,
        "total_shares":      total_shares,
        "total_checkins":    total_checkins,
        "taxa_conversao":    taxa_conversao,
        "taxa_save":         taxa_save,
        "taxa_compartilhar": taxa_compartilhar,
        "taxa_retencao":     taxa_retencao,
        "taxa_uso_promo":    taxa_uso_promo,
        "retencao":          retencao,
    }
