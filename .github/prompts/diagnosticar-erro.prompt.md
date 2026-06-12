---
mode: ask
description: Diagnostica e corrige erros comuns no dashboard Explori — desde erros de carregamento de dados até gráficos em branco ou quebrados. Use ao encontrar qualquer erro no terminal ou no dashboard.
---

Diagnostique e corrija o seguinte erro no dashboard Explori.

**Arquivo com erro:** ${input:arquivo:Ex: dashboard_donos.py}
**Contexto onde ocorreu:** ${input:contexto:Ex: ao carregar a tela de retenção, ao executar streamlit run, ao filtrar por categoria}
**Mensagem de erro (cole abaixo):**

---

## Protocolo de Diagnóstico

Siga os passos na ordem abaixo, do mais provável para o menos provável:

### Passo 1 — Erros de Pipeline de Dados

Verificar se o erro ocorre na carga ou transformação dos dados:

| Sintoma | Causa provável | Correção padrão |
|---------|----------------|-----------------|
| `KeyError: 'coluna'` | coluna com nome diferente após merge | `df.columns.tolist()` para inspecionar |
| `ValueError: cannot convert float NaN` | nulo não tratado antes de `astype(int)` | `.fillna(0).astype(int)` |
| `FileNotFoundError` no ZIP | caminho do ZIP incorreto | verificar `DATA_PATH` relativo ao `cwd` |
| `EmptyDataError` | CSV vazio no ZIP | adicionar `if df.empty: st.error(...)` |
| Gráfico em branco sem erro | DataFrame vazio chegou ao `px.*` | verificar `if not df.empty` antes do plot |
| `DtypeWarning` | tipo misto na coluna | forçar `dtype=str` no `pd.read_csv` |
| `observed` warning do Pandas | `.groupby()` em coluna categórica sem `observed=` | adicionar `observed=False` |

### Passo 2 — Erros de Streamlit

| Sintoma | Causa provável | Correção |
|---------|----------------|---------|
| `StreamlitAPIException: set_page_config` | `st.set_page_config` não é a primeira chamada | mover para linha 1, antes de qualquer import customizado |
| Sidebar não aparece | `st.sidebar.*` antes de `st.set_page_config` | reordenar |
| `CachedStFunctionWarning` | `st.*` dentro de `@st.cache_data` | remover chamadas Streamlit de dentro do cache |
| Loop infinito na sessão | mutação de `st.session_state` dentro de callback | usar `on_change` corretamente |

### Passo 3 — Erros de Plotly

| Sintoma | Causa provável | Correção |
|---------|----------------|---------|
| `ValueError: Wide-form` | DataFrame em formato wide ao invés de long | usar `pd.melt()` antes do `px.*` |
| Cores incorretas | `color=` aponta para coluna string sem `color_discrete_map` | adicionar mapeamento explícito |
| Texto fora dos limites | `textposition="outside"` sem espaço no eixo | `fig.update_layout(yaxis=dict(range=[0, max*1.15]))` |

---

## Formato de entrega

```
🔍 DIAGNÓSTICO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Causa raiz identificada: [explicação]
Passo onde ocorreu: [ Carga de dados | Transformação | Plot | Streamlit ]

📍 Trecho problemático:
[código com o problema]

✅ Correção aplicada:
[código corrigido]

🧪 Como testar:
[instrução para verificar que o erro foi resolvido]

⚠️ Verificações adicionais recomendadas:
[outros pontos que podem estar afetados pelo mesmo problema]
```

Se o erro **não se enquadrar** nos padrões acima, peça o traceback completo e as primeiras 20 linhas da função `carregar_dados()` para diagnóstico aprofundado.
