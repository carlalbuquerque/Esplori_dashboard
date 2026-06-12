---
description: Schema completo das 6 tabelas CSV do dataset Explori. Ativa automaticamente em qualquer contexto do projeto para garantir que nomes de colunas, tipos e tratamentos estejam sempre corretos.
alwaysApply: true
---

# Schema do Dataset Explori — Fonte Única de Verdade

O dataset da plataforma Explori é composto por **6 tabelas CSV** extraídas de `data/dataset_eda_ficticio.zip`. Todos os nomes de colunas, tipos e regras de tratamento abaixo são canônicos — nunca invente ou renomeie colunas.

---

## `usuarios.csv`

| Coluna | Tipo | Regra de tratamento |
|--------|------|---------------------|
| `id_usuario` | int | Chave primária — **nunca exibir ao usuário final** |
| `idade` | int | `dropna()` + filtro `18 <= idade <= 65` |
| `genero` | str | `.fillna("não informado")` |
| `origem_geografica` | str | `.fillna(moda)` + `.str.lower().str.strip()` |
| `horario_maior_busca` | str → datetime | `pd.to_datetime(..., format="%H:%M:%S", errors="coerce")` → extrair `.dt.hour` |
| `efetuou_checkin` | bool | `.fillna(False).astype(bool)` |

**Coluna derivada obrigatória:**
```python
usuarios["faixa_etaria"] = pd.cut(
    usuarios["idade"],
    bins=[18, 25, 35, 45, 55, 65],
    labels=["18-25", "26-35", "36-45", "46-55", "56-65"],
    include_lowest=True,
)
```

---

## `estabelecimentos.csv`

| Coluna | Tipo | Regra de tratamento |
|--------|------|---------------------|
| `id_estabelecimento` | int | Chave primária — **nunca exibir ao usuário final** |
| `nome_estabelecimento` | str | Sem tratamento especial |
| `origem_geografica` | str | `.str.lower().str.strip()` |
| `faixa_de_gasto` | str | Valores válidos: `"baixo"`, `"medio"`, `"alto"` |
| `criacao_promocoes` | int | `.fillna(0)` |

---

## `categorias.csv`

| Coluna | Tipo | Regra de tratamento |
|--------|------|---------------------|
| `id_categoria` | int | Chave primária |
| `nome_categoria` | str | Sem tratamento especial |

---

## `estabelecimento_categoria.csv`

| Coluna | Tipo | Regra de tratamento |
|--------|------|---------------------|
| `id_estabelecimento` | int | FK → `estabelecimentos.csv` |
| `id_categoria` | int | FK → `categorias.csv` |

Tabela de junção N:N. Usar para cruzar estabelecimentos com suas categorias.

---

## `checkins.csv`

| Coluna | Tipo | Regra de tratamento |
|--------|------|---------------------|
| `id_checkin` | int | Chave primária — **nunca exibir ao usuário final** |
| `id_usuario` | int | FK → `usuarios.csv` — **nunca exibir ao usuário final** |
| `id_estabelecimento` | int | FK → `estabelecimentos.csv` — **nunca exibir ao usuário final** |
| `id_categoria` | int | FK → `categorias.csv` |
| `data_hora_checkin` | str → datetime | `pd.to_datetime(..., errors="coerce")` |
| `faixa_gasto` | str | Valores: `"baixo"`, `"medio"`, `"alto"` |
| `usou_voucher` | bool | Sem tratamento especial |

**Limpeza obrigatória:**
```python
checkins.dropna(inplace=True)
checkins.drop_duplicates(inplace=True)
```

---

## `interacoes.csv`

| Coluna | Tipo | Regra de tratamento |
|--------|------|---------------------|
| `id_usuario` | int | FK → `usuarios.csv` — **nunca exibir ao usuário final** |
| `id_estabelecimento` | int | FK → `estabelecimentos.csv` — **nunca exibir ao usuário final** |
| `visualizacoes_perfil` | int | `.fillna(0).astype(int)` |
| `saves_favoritos` | int | `.fillna(0).astype(int)` |
| `compartilhamentos` | int | `.fillna(0).astype(int)` |

---

## `promocoes.csv`

| Coluna | Tipo | Regra de tratamento |
|--------|------|---------------------|
| `id_promocao` | int | Chave primária — **nunca exibir ao usuário final** |
| `id_estabelecimento` | int | FK → `estabelecimentos.csv` |
| `quantidade_disponibilizada` | float | `.fillna(mediana)` |
| `quantidade_utilizada` | float | Não pode exceder `quantidade_disponibilizada`: `min(axis=1)` |

**Coluna derivada obrigatória:**
```python
promocoes["taxa_uso"] = (
    promocoes["quantidade_utilizada"] / promocoes["quantidade_disponibilizada"]
)
```

---

## Joins Mais Usados no Dashboard

```python
# Engajamento por estabelecimento
df_eng = interacoes.merge(estab, on="id_estabelecimento", how="left")

# Check-ins com categoria
df_cat = checkins.merge(categorias, on="id_categoria", how="left")

# Verificar se interação resultou em check-in
df_funil = interacoes.merge(
    checkins, on=["id_usuario", "id_estabelecimento"], how="left"
)
df_funil["fez_checkin"] = df_funil["id_checkin"].notnull()

# Concorrência: estabelecimento + categoria + faixa de gasto
df_conc = estab_cat.merge(estab, on="id_estabelecimento").merge(categorias, on="id_categoria")
```

---

## Volumes de Referência (pós-limpeza)

| Tabela | Registros válidos |
|--------|------------------|
| `usuarios` | ~5.673 |
| `interacoes` | ~20.002 |
| `checkins` | < 20.002 (após dropna) |
| `estabelecimentos` | estável (sem duplicatas) |
