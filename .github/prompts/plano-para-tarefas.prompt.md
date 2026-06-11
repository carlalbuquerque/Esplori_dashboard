---
mode: ask
description: Decompõe um plan.md em tarefas atômicas com dependências, estimativas e critérios de done. Use após spec-para-plano e antes de acionar @dashboard-builder para implementação.
---

Decomponha o plano de implementação abaixo em tarefas atômicas prontas para execução.

**Funcionalidade:** ${input:nomeFuncionalidade:Ex: Análise de Retenção de Clientes}
**Caminho do plan.md:** ${input:caminhoPlan:Ex: documento projeto/documentos/planos/retencao/plan.md}
**Executor principal:** ${input:executor:Ex: @dashboard-builder | @data-analyst | eu mesmo}

> **Regra de atomicidade:** Uma tarefa é atômica quando pode ser implementada, testada e revertida de forma independente em uma única sessão de trabalho (≤ 2h). Se uma tarefa exceder isso, ela deve ser dividida.

---

## Protocolo de Decomposição

Execute os 4 passos abaixo na ordem exata.

---

### Passo 1 — Inventário do plan.md

Leia o `${input:caminhoPlan}` e extraia:
- Total de fases e tarefas identificadas
- Dependências implícitas entre tarefas
- Componentes Streamlit/Plotly que serão criados ou modificados
- Tabelas do dataset necessárias

Apresente um resumo antes de continuar:

```
INVENTÁRIO — ${input:nomeFuncionalidade}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fases: X  |  Tarefas no plan.md: Y
Componentes novos: Z  |  Componentes modificados: W
Tabelas do dataset: [lista]
```

---

### Passo 2 — Criação das Tarefas Atômicas

Para cada tarefa identificada, gere um bloco no formato abaixo:

```
---
### TASK-[NN]: [título imperativo e específico]

**Fase:** [1-Dados | 2-KPIs | 3-Interface | 4-Visualizações | 5-Validação]
**Executor:** ${input:executor}
**Estimativa:** [S = <30min | M = 30–60min | L = 60–120min]
**Depende de:** [TASK-XX, TASK-YY | nenhuma]
**Bloqueia:** [TASK-XX, TASK-YY | nenhuma]

**Escopo exato (o que ENTRA):**
- [item 1]
- [item 2]

**Fora do escopo (o que NÃO entra):**
- [item 1 — pertence a TASK-XX]

**Critérios de Done:**
- [ ] [critério verificável e binário — passa ou não passa]
- [ ] [critério verificável e binário]
- [ ] `streamlit run dashboard_donos.py` executa sem erros após esta tarefa

**Artefatos produzidos:**
- [arquivo modificado / criado: caminho/relativo]

**Artigo(s) da Constituição aplicável(eis):**
- Art. X — [nome] ([regra específica aplicada nesta tarefa])
---
```

---

### Passo 3 — Grafo de Dependências

Após listar todas as tarefas, gere o grafo de dependências em texto:

```
GRAFO DE DEPENDÊNCIAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[início]
    │
    ▼
TASK-01 (S) → TASK-02 (M) → TASK-04 (M) ──┐
                                            ├──▶ TASK-07 (L) → [fim]
TASK-03 (S) ──────────────────────────────┘

Caminho crítico: TASK-01 → TASK-02 → TASK-04 → TASK-07
Tempo total estimado: ~Xh (otimista) | ~Yh (pessimista)
Tarefas paralelizáveis: TASK-01 ∥ TASK-03
```

---

### Passo 4 — Tabela de Critérios de Done Consolidados

Gere uma tabela com **todos** os critérios de done, agrupados por categoria:

```markdown
## Critérios de Done Consolidados

### Dados e Pipeline (Artigos 3, 4, 7)
| TASK | Critério | Como verificar |
|------|---------|---------------|
| TASK-01 | `@st.cache_data` presente em `carregar_dados()` | Inspecionar decorador na função |
| TASK-02 | Nulos tratados antes de qualquer cálculo | Executar `df.isnull().sum()` e confirmar 0 |
| TASK-02 | `observed=False` em todo `.groupby()` categórico | Buscar `groupby` no arquivo |

### Interface Streamlit (Artigos 2, 5, 9)
| TASK | Critério | Como verificar |
|------|---------|---------------|
| TASK-05 | `st.set_page_config()` é a primeira linha executável | Verificar linha 1 do arquivo |
| TASK-06 | Nova tela adicionada ao sidebar de navegação | Navegar no browser e confirmar |
| TASK-06 | `if not df.empty:` antes de cada `px.*` | Buscar `px.` e verificar guarda acima |

### Visualizações Plotly (Artigo 8)
| TASK | Critério | Como verificar |
|------|---------|---------------|
| TASK-08 | Apenas cores da paleta Explori em uso | Buscar `#` no código e comparar com paleta |
| TASK-08 | `plot_bgcolor="white"` e `paper_bgcolor="white"` | Inspecionar `update_layout` |
| TASK-08 | `st.plotly_chart(fig, use_container_width=True)` | Buscar `plotly_chart` no arquivo |
| TASK-09 | `insight-box` presente abaixo de cada gráfico | Buscar `insight-box` no arquivo |

### KPIs e Métricas (Artigos 3, 4)
| TASK | Critério | Como verificar |
|------|---------|---------------|
| TASK-03 | Fórmula canônica utilizada (sem hardcode) | Comparar com `copilot-instructions.md` |
| TASK-03 | `delta=` com benchmark nos `st.metric()` | Inspecionar chamadas `st.metric` |
| TASK-03 | Valor calculado do dataset (não simulado) | Rastrear origem da variável |

### Segurança e LGPD (Artigo 6)
| TASK | Critério | Como verificar |
|------|---------|---------------|
| Todas | `id_usuario`, `id_estabelecimento` não aparecem na UI | Buscar `id_` em `st.dataframe/table/write` |
| Todas | Dados individuais só em forma agregada | Verificar ausência de `.iterrows()` na UI |

### CI/CD — Sacred CI (Artigo 5)
| TASK | Critério | Como verificar |
|------|---------|---------------|
| Todas | `streamlit run dashboard_donos.py` sem erros | Executar e navegar todas as telas |
| Todas | Nenhum `DeprecationWarning` do Streamlit | Inspecionar terminal após `streamlit run` |
```

---

## Formato Final de Entrega — `tasks.md`

Consolide tudo em um único arquivo `tasks.md` com esta estrutura:

```markdown
# Tarefas: ${input:nomeFuncionalidade}

**Origem:** ${input:caminhoPlan}  
**Total de tarefas:** N  
**Estimativa total:** Xh–Yh  
**Status:** 🔴 Não iniciado

---

## Resumo de Progresso

| # | Tarefa | Fase | Est. | Depende de | Status |
|---|--------|------|------|-----------|--------|
| TASK-01 | [título] | Dados | S | — | ⬜ |
| TASK-02 | [título] | Dados | M | TASK-01 | ⬜ |
...

---

## Tarefas Detalhadas

[bloco de cada TASK conforme Passo 2]

---

## Grafo de Dependências

[conforme Passo 3]

---

## Critérios de Done Consolidados

[tabela conforme Passo 4]

---

## Instrução para o Executor

Para iniciar a implementação com @dashboard-builder:

> "@dashboard-builder, implemente TASK-01 conforme descrito em `tasks.md`.
> Escopo: [escopo exato].
> Done quando: [critérios de done da TASK-01]."
```

Salve o arquivo como `${input:caminhoPlan}/../tasks.md` e confirme a criação.
