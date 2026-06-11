---
mode: ask
description: Gera os 5 artefatos de planejamento (plan.md, data-model.md, contracts/, research.md, quickstart.md) a partir de um spec.md aprovado. Use após o prompt requisito-para-spec e antes de qualquer implementação.
---

Gere o pacote completo de artefatos de planejamento para a funcionalidade especificada abaixo.

**Funcionalidade (nome exato do spec):** ${input:nomeFuncionalidade:Ex: Análise de Retenção de Clientes}
**Caminho do spec aprovado:** ${input:caminhoSpec:Ex: documento projeto/documentos/specs/spec-retencao.md}
**Diretório de saída dos artefatos:** ${input:diretorioSaida:Ex: documento projeto/documentos/planos/retencao}

> **Pré-condição:** O spec deve estar aprovado — todas as `[NEEDS CLARIFICATION]` resolvidas e checklist de pré-implementação completo. Se houver itens abertos, pare e resolva antes de continuar.

---

## Artefato 1 — `plan.md` (Plano de Implementação)

Gere um plano de implementação sequencial com as seguintes seções:

```markdown
# Plano de Implementação: [nomeFuncionalidade]

**Origem:** [caminhoSpec]  
**Estimativa:** [N tarefas, estimativa em sessões de trabalho]  
**Ordem de execução:** sequencial (cada tarefa depende da anterior)

---

## Fase 1 — Preparação de Dados
- [ ] TASK-01: Validar disponibilidade das colunas necessárias no dataset
- [ ] TASK-02: Implementar/estender `carregar_dados()` com as novas transformações
- [ ] TASK-03: Validar pipeline com `assert not df.empty` e range checks

## Fase 2 — Cálculo de KPIs
- [ ] TASK-04: Implementar cálculos usando fórmulas canônicas
- [ ] TASK-05: Comparar resultados com benchmarks (conversão ≥35%, save ≥12%, compartilhamento ≥4%)
- [ ] TASK-06: Validar outputs com `assert valor.between(0, 1).all()`

## Fase 3 — Interface (Streamlit)
- [ ] TASK-07: Criar bloco `elif pagina == "..."` na navegação
- [ ] TASK-08: Implementar filtros da tela (sidebar ou inline)
- [ ] TASK-09: Implementar cards de KPI com `st.metric()` e `delta=`

## Fase 4 — Visualizações (Plotly)
- [ ] TASK-10: Implementar gráfico principal com paleta Explori
- [ ] TASK-11: Adicionar `insight-box` abaixo de cada gráfico
- [ ] TASK-12: Aplicar `plot_bgcolor="white"`, `paper_bgcolor="white"`

## Fase 5 — Validação Final
- [ ] TASK-13: Executar `streamlit run dashboard_donos.py` sem erros (Artigo 5 — Sacred CI)
- [ ] TASK-14: Navegar pela tela com dados reais e verificar todos os gráficos
- [ ] TASK-15: Revisar com `@security-reviewer` (verificar exposição de IDs)

---

## Rastreabilidade

| TASK | Story(s) | AC(s) | Artigo Constituição |
|------|----------|-------|---------------------|
| TASK-01 | US-01 | AC-01 | Art. 4 — No Mocks |
| TASK-02 | US-01, US-02 | AC-01, AC-02 | Art. 7 — Cache-Always |
...

---

## Riscos e Dependências
[Listar dependências entre tarefas e riscos identificados no spec]
```

---

## Artefato 2 — `data-model.md` (Modelo de Dados)

Documente o modelo de dados específico para esta funcionalidade:

```markdown
# Modelo de Dados: [nomeFuncionalidade]

## Tabelas Consumidas

### [nome_tabela]
| Coluna | Tipo | Nulos permitidos | Tratamento aplicado | Uso nesta funcionalidade |
|--------|------|-----------------|--------------------|-----------------------|
| coluna_a | str | Não | `.str.lower().str.strip()` | Filtro de categoria |
| coluna_b | int | Sim → 0 | `.fillna(0).astype(int)` | Cálculo de KPI X |

## Colunas Derivadas

| Nome | Fórmula | Tipo resultado | Exemplo |
|------|---------|---------------|---------|
| `faixa_etaria` | `pd.cut(df["idade"], bins=[18,25,35,45,55,65])` | Categorical | "26-35" |
| `taxa_retencao` | `(df["num_checkins"] >= 2).sum() / len(df)` | float | 0.1636 |

## Joins Necessários

```python
# Join canônico para esta funcionalidade
df_base = checkins.merge(usuarios, on="id_usuario", how="left")
df_base = df_base.merge(interacoes, on=["id_usuario", "id_estabelecimento"], how="left")
```

## Volumes Esperados (pós-limpeza)

| Tabela | Linhas esperadas | Observação |
|--------|-----------------|-----------|
| `usuarios` | ~5.673 | após drop de idades fora de 18-65 |
| `checkins` | ~8.000+ | apenas `efetuou_checkin == True` |
| `interacoes` | ~20.002 | após `.fillna(0)` nas métricas |

## Alertas de Qualidade

- [ASSUMPTION] ou [CONFIRMED] para cada premissa sobre os dados
- Listar correlações conhecidas: saves→checkins (r≈0.28), visualizações→saves (r≈0.18)
```

---

## Artefato 3 — `contracts/` (Contratos de Interface)

Crie **um arquivo por componente visual** na subpasta `contracts/`:

### `contracts/[nome-componente].md`

```markdown
# Contrato: [Nome do Componente]

**Tipo:** [KPI Card | Gráfico de Barras | Tabela | Filtro | Gráfico de Funil | ...]  
**Story:** US-XX  
**AC:** AC-XX

---

## Entradas (Inputs)

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `df` | pd.DataFrame | Sim | — | DataFrame pós-limpeza com colunas X, Y, Z |
| `periodo` | tuple[date, date] | Não | últimos 30 dias | Filtro de período |

## Saídas (Outputs)

| Saída | Descrição |
|-------|-----------|
| `st.metric()` | Card com valor atual, delta vs benchmark |
| `st.plotly_chart()` | Gráfico X com paleta Explori |
| `st.markdown(insight-box)` | Texto de insight gerado dinamicamente |

## Comportamento em Casos Extremos

| Situação | Comportamento esperado |
|----------|----------------------|
| `df.empty` | `st.info("Nenhum dado encontrado...")` |
| Valor de KPI = 0 | Exibir 0% com delta negativo |
| Apenas 1 registro | Gráfico renderiza, sem erro |

## Paleta Aplicada

```python
color_discrete_sequence = [COR_PRIMARIA, COR_SECUNDARIA, COR_VERDE, COR_NEUTRO]
# COR_PRIMARIA = "#E07A2F" | COR_SECUNDARIA = "#B96A4A"
# COR_VERDE = "#6B7A3A"   | COR_NEUTRO = "#8A9450"
```
```

> Criar um arquivo `contracts/` por gráfico e por card de KPI identificados no spec.

---

## Artefato 4 — `research.md` (Achados de Pesquisa)

Consolide os dados já conhecidos relevantes para esta funcionalidade:

```markdown
# Research: [nomeFuncionalidade]

## Insights Estratégicos Aplicáveis

Liste quais dos 7 insights confirmados são relevantes para esta tela:

| # | Insight | Relevância para esta funcionalidade |
|---|---------|-------------------------------------|
| 1 | Pico 13h–16h, spike às 14h | [alta / média / baixa] — [justificativa] |
| 2 | 84% fazem apenas 1 check-in | [alta / média / baixa] — [justificativa] |
| 3 | ~46% dos usuários são de Recife | [alta / média / baixa] — [justificativa] |
| 4 | Saves antecedem check-ins (+29.4%, r≈0.28) | [alta / média / baixa] — [justificativa] |
| 5 | Maioria das promoções não atinge 100% de uso | [alta / média / baixa] — [justificativa] |
| 6 | Faixa "baixo" domina em todas as categorias | [alta / média / baixa] — [justificativa] |
| 7 | Funil clássico; compartilhamentos r≈0.07 | [alta / média / baixa] — [justificativa] |

## Benchmarks Aplicáveis

| KPI | Benchmark | Fonte |
|-----|-----------|-------|
| Taxa de conversão | ≥ 35% | Análise exploratória Explori 2025-2026 |
| Taxa de save | ≥ 12% | Análise exploratória Explori 2025-2026 |
| Taxa de compartilhamento | ≥ 4% | Análise exploratória Explori 2025-2026 |

## Correlações Confirmadas

| Variável A | Variável B | r | Interpretação |
|-----------|-----------|---|--------------|
| saves_favoritos | efetuou_checkin | ≈ 0.28 | Fraca positiva |
| visualizacoes_perfil | saves_favoritos | ≈ 0.18 | Fraca positiva |
| compartilhamentos | efetuou_checkin | ≈ 0.07 | Muito fraca |

## Perguntas Abertas para Investigação

[Listar hipóteses não confirmadas que podem enriquecer a análise desta tela]
```

---

## Artefato 5 — `quickstart.md` (Guia de Início Rápido)

Guia operacional para qualquer desenvolvedor reproduzir e validar a funcionalidade:

```markdown
# Quickstart: [nomeFuncionalidade]

## Pré-requisitos

```bash
# 1. Clonar o repositório e entrar na pasta
cd Explori_dashboard

# 2. Instalar dependências (Artigo 2 — CLI Mandate)
pip install -r requirements.txt

# 3. Verificar que o dataset está presente
# Deve existir: data/dataset_eda_ficticio.zip
```

## Executar o Dashboard

```bash
streamlit run dashboard_donos.py
```

Acessar: http://localhost:8501  
Navegar até: **[ícone] [nomeFuncionalidade]** no menu lateral

## Validar a Funcionalidade

Checklist de validação manual:

- [ ] Página carrega sem erro no console
- [ ] [KPI principal] exibe valor calculado (não hardcoded)
- [ ] Delta vs benchmark aparece no `st.metric()`
- [ ] Gráfico principal renderiza com cores Explori (laranja `#E07A2F`)
- [ ] `insight-box` aparece abaixo do gráfico
- [ ] Filtrar por período altera os valores corretamente
- [ ] Filtrar até restar 0 registros exibe `st.info(...)`, não erro

## Reproduzir o Cálculo dos KPIs

```python
# Cole no terminal Python para validar manualmente:
import pandas as pd, zipfile, os

with zipfile.ZipFile("data/dataset_eda_ficticio.zip") as z:
    checkins   = pd.read_csv(z.open("checkins.csv"))
    interacoes = pd.read_csv(z.open("interacoes.csv"))

# [Inserir fórmula canônica do KPI principal desta funcionalidade]
# Ex:
taxa = len(checkins[checkins["efetuou_checkin"] == True]) / interacoes["visualizacoes_perfil"].sum()
print(f"Taxa de conversão: {taxa:.1%}")  # Esperado: ~[valor] | Meta: ≥35%
```

## Troubleshooting Comum

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Gráfico em branco | DataFrame vazio após filtro | Verificar `if not df.empty` |
| `KeyError: 'coluna'` | Nome de coluna errado | Confirmar com `df.columns.tolist()` |
| `set_page_config` error | Não é a primeira linha | Mover para linha 1 do arquivo |
| Cache desatualizado | Dados antigos em memória | `st.cache_data.clear()` no browser |
```

---

## Instrução Final de Entrega

Gere os 5 artefatos na estrutura de pastas abaixo e confirme cada arquivo criado:

```
${input:diretorioSaida}/
├── plan.md                          ← Plano de implementação com TASKs
├── data-model.md                    ← Esquema de dados e transformações
├── contracts/
│   ├── kpi-[nome].md               ← Um arquivo por card de KPI
│   └── grafico-[nome].md           ← Um arquivo por gráfico
├── research.md                      ← Insights e benchmarks aplicáveis
└── quickstart.md                    ← Guia de execução e validação
```

Após criar todos os arquivos, imprima o resumo:

```
ARTEFATOS GERADOS — ${input:nomeFuncionalidade}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ plan.md         — X tarefas em Y fases
✅ data-model.md   — X tabelas, Y colunas derivadas
✅ contracts/      — X arquivos (Y KPIs + Z gráficos)
✅ research.md     — X insights aplicáveis
✅ quickstart.md   — checklist de N itens

Próximo passo: implementar TASK-01 com @dashboard-builder
```
