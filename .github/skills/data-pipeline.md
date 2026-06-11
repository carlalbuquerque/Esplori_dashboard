---
description: Pipeline de carregamento, limpeza e preparação dos dados do dataset Explori. Ativada em arquivos Python com o padrão canônico da função carregar_dados() e todas as transformações intermediárias necessárias antes de calcular KPIs ou plotar gráficos.
applyTo: "**/*.py"
---

# Pipeline de Dados — Explori Dashboard

Esta skill define o pipeline canônico de carregamento e limpeza dos dados. **Toda lógica de `carregar_dados()` deve seguir exatamente esta ordem.** Nunca calcule KPIs ou gere gráficos a partir de dados não tratados.

---

## Regra de Ouro

```
EXTRAIR → LIMPAR → VALIDAR → DERIVAR COLUNAS → CALCULAR KPIs → PLOTAR
```

Nenhuma etapa pode ser pulada ou invertida.

---

## Função `carregar_dados()` — Implementação Canônica

```python
@st.cache_data
def carregar_dados():
    """
    Carrega e trata todos os CSVs do dataset Explori.
    Retorna: (usuarios, estab, categorias, estab_cat, checkins, interacoes, promocoes)
    """
    import zipfile, os

    # ─── 1. LOCALIZAR E EXTRAIR O ZIP ─────────────────────────────
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    data_dir  = os.path.join(base_dir, "data")
    zip_path  = next(
        (os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".zip")),
        None,
    )
    extract_dir = os.path.join(data_dir, "extracted")

    if zip_path and not os.path.exists(extract_dir):
        # Proteção contra path traversal no ZIP
        with zipfile.ZipFile(zip_path, "r") as z:
            for member in z.namelist():
                member_path = os.path.realpath(os.path.join(extract_dir, member))
                if not member_path.startswith(os.path.realpath(extract_dir)):
                    raise ValueError(f"Path traversal detectado no ZIP: {member}")
            z.extractall(extract_dir)

    # ─── 2. HELPER DE LEITURA ─────────────────────────────────────
    csv_dir = extract_dir if os.path.exists(extract_dir) else data_dir

    def _read(name: str) -> pd.DataFrame:
        for root, _, files in os.walk(csv_dir):
            for fn in files:
                if fn == name:
                    return pd.read_csv(os.path.join(root, fn))
        return pd.DataFrame()

    # ─── 3. CARREGAR TABELAS ──────────────────────────────────────
    usuarios   = _read("usuarios.csv")
    estab      = _read("estabelecimentos.csv")
    categorias = _read("categorias.csv")
    estab_cat  = _read("estabelecimento_categoria.csv")
    checkins   = _read("checkins.csv")
    interacoes = _read("interacoes.csv")
    promocoes  = _read("promocoes.csv")

    # ─── 4. TRATAR USUARIOS ───────────────────────────────────────
    if not usuarios.empty:
        # Padronização textual
        if "origem_geografica" in usuarios.columns:
            usuarios["origem_geografica"] = (
                usuarios["origem_geografica"].str.lower().str.strip()
            )
        # Nulos
        usuarios["genero"] = usuarios["genero"].fillna("não informado")
        usuarios["efetuou_checkin"] = (
            usuarios["efetuou_checkin"].fillna(False).astype(bool)
        )
        if "origem_geografica" in usuarios.columns:
            moda = usuarios["origem_geografica"].mode()[0]
            usuarios["origem_geografica"] = (
                usuarios["origem_geografica"].fillna(moda)
            )
        # Idade: remover nulos e outliers
        usuarios.dropna(subset=["idade"], inplace=True)
        usuarios["idade"] = usuarios["idade"].astype(int)
        usuarios = usuarios[(usuarios["idade"] >= 18) & (usuarios["idade"] <= 65)]
        # Duplicatas
        usuarios.drop_duplicates(inplace=True)
        # Coluna derivada: faixa_etaria
        usuarios["faixa_etaria"] = pd.cut(
            usuarios["idade"],
            bins=[18, 25, 35, 45, 55, 65],
            labels=["18-25", "26-35", "36-45", "46-55", "56-65"],
            include_lowest=True,
        )
        # Coluna derivada: hora de pico
        if "horario_maior_busca" in usuarios.columns:
            usuarios["horario_maior_busca"] = pd.to_datetime(
                usuarios["horario_maior_busca"],
                format="%H:%M:%S",
                errors="coerce",
            )
            usuarios["hora"] = usuarios["horario_maior_busca"].dt.hour

    # ─── 5. TRATAR ESTABELECIMENTOS ───────────────────────────────
    if not estab.empty:
        if "origem_geografica" in estab.columns:
            estab["origem_geografica"] = (
                estab["origem_geografica"].str.lower().str.strip()
            )
        estab["criacao_promocoes"] = estab["criacao_promocoes"].fillna(0)
        estab.drop_duplicates(inplace=True)

    # ─── 6. TRATAR CHECKINS ───────────────────────────────────────
    if not checkins.empty:
        if "data_hora_checkin" in checkins.columns:
            checkins["data_hora_checkin"] = pd.to_datetime(
                checkins["data_hora_checkin"], errors="coerce"
            )
        checkins.dropna(inplace=True)
        checkins.drop_duplicates(inplace=True)

    # ─── 7. TRATAR INTERAÇÕES ─────────────────────────────────────
    if not interacoes.empty:
        for col in ["visualizacoes_perfil", "saves_favoritos", "compartilhamentos"]:
            if col in interacoes.columns:
                interacoes[col] = interacoes[col].fillna(0).astype(int)
        interacoes.drop_duplicates(inplace=True)

    # ─── 8. TRATAR PROMOÇÕES ──────────────────────────────────────
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
            # Consistência lógica: utilizada não pode exceder disponibilizada
            promocoes["quantidade_utilizada"] = promocoes[
                ["quantidade_utilizada", "quantidade_disponibilizada"]
            ].min(axis=1)
            # Coluna derivada: taxa_uso
            promocoes["taxa_uso"] = (
                promocoes["quantidade_utilizada"]
                / promocoes["quantidade_disponibilizada"]
            )
        promocoes.drop_duplicates(inplace=True)

    return usuarios, estab, categorias, estab_cat, checkins, interacoes, promocoes
```

---

## Calcular KPIs — Após o Pipeline

Só calcule KPIs **após** chamar `carregar_dados()` e verificar que os DataFrames não estão vazios:

```python
usuarios, estab, categorias, estab_cat, checkins, interacoes, promocoes = carregar_dados()

# Verificação de sanidade antes de qualquer cálculo
if interacoes.empty or checkins.empty:
    st.warning("Dados insuficientes para calcular KPIs.")
    st.stop()

# KPIs canônicos
total_views      = interacoes["visualizacoes_perfil"].sum()
total_saves      = interacoes["saves_favoritos"].sum()
total_shares     = interacoes["compartilhamentos"].sum()
total_checkins   = len(checkins)

taxa_conversao   = total_checkins / total_views if total_views > 0 else 0
taxa_save        = total_saves / total_views if total_views > 0 else 0
taxa_compartilhar = total_shares / total_views if total_views > 0 else 0

if not promocoes.empty and "taxa_uso" in promocoes.columns:
    taxa_uso_promo = promocoes["taxa_uso"].mean()

retencao = checkins.groupby("id_usuario").size().reset_index(name="num_checkins")
taxa_retencao = (retencao["num_checkins"] >= 2).sum() / len(retencao) if len(retencao) > 0 else 0
```

---

## Joins Comuns — Padrão Seguro

```python
# ─── Engajamento por estabelecimento ──────────────────────────
if not interacoes.empty and not estab.empty:
    df_eng = interacoes.merge(estab, on="id_estabelecimento", how="left")

# ─── Funil: verificar se interação virou check-in ─────────────
if not interacoes.empty and not checkins.empty:
    df_funil = interacoes.merge(
        checkins[["id_usuario", "id_estabelecimento", "id_checkin"]],
        on=["id_usuario", "id_estabelecimento"],
        how="left",
    )
    df_funil["fez_checkin"] = df_funil["id_checkin"].notnull()

# ─── Check-ins com nome de categoria ──────────────────────────
if not checkins.empty and not categorias.empty:
    df_cat = checkins.merge(categorias, on="id_categoria", how="left")

# ─── Retenção por usuário ─────────────────────────────────────
if not checkins.empty:
    retencao = checkins.groupby("id_usuario").size().reset_index(name="num_checkins")
```

---

## Tratamento de Erros na Carga

```python
try:
    usuarios, estab, categorias, estab_cat, checkins, interacoes, promocoes = carregar_dados()
    dados_ok = not usuarios.empty
except Exception as e:
    dados_ok = False
    st.error(f"Erro ao carregar dados: {e}")

if not dados_ok:
    st.warning(
        "⚠️ Dataset não encontrado. "
        "Coloque o arquivo ZIP na pasta `data/` e reinicie o app."
    )
    st.stop()
```
