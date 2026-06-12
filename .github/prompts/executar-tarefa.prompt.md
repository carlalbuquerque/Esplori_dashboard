---
mode: agent
description: Executa uma tarefa atômica do tasks.md seguindo rigorosamente a Constituição do projeto — Library-First, Test-First, No Mocks e Sacred CI. Use com @dashboard-builder para implementar cada TASK individualmente.
---

Execute a tarefa abaixo seguindo os 4 princípios constitucionais do projeto Explori.

**Tarefa a executar:** ${input:taskId:Ex: TASK-03}
**Título da tarefa:** ${input:taskTitulo:Ex: Implementar cálculo de taxa de retenção}
**Caminho do tasks.md:** ${input:caminhoTasks:Ex: documento projeto/documentos/planos/retencao/tasks.md}
**Arquivo(s) a modificar:** ${input:arquivos:Ex: dashboard_donos.py}

> Leia o bloco completo da `${input:taskId}` no `${input:caminhoTasks}` antes de escrever qualquer linha de código. O escopo exato e os critérios de done estão lá — não assuma nada além do que está documentado.

---

## Princípio 1 — Library-First (Artigo 1 da Constituição)

**Antes de escrever qualquer código, responda:**

| Necessidade | Solução de biblioteca disponível | Código customizado necessário? |
|------------|----------------------------------|-------------------------------|
| Layout em colunas | `st.columns()` | Não |
| Gráfico de barras | `px.bar()` | Não |
| Métrica com delta | `st.metric()` | Não |
| Formatação de % | `f"{valor:.1%}"` | Não |
| Filtro de data | `st.date_input()` | Não |
| Agrupamento | `df.groupby().agg()` | Não |
| Merge de tabelas | `df.merge()` | Não |

**Regra:** Se a biblioteca resolve, use a biblioteca. Só escreva código customizado para lógica de negócio que não existe em nenhuma das bibliotecas aprovadas (Streamlit, Plotly, Pandas).

Stack aprovada — não instalar nada além disso:
```
streamlit>=1.32.0
plotly>=5.18.0
pandas>=2.0.0
```

---

## Princípio 2 — Test-First (Artigo 3 da Constituição)

**Execute as validações na ordem abaixo ANTES de plotar ou exibir qualquer dado:**

### 2a. Validar disponibilidade dos dados
```python
# Cole este bloco no início da função/tela, antes de qualquer lógica
assert not df.empty, f"[TASK ${input:taskId}] DataFrame vazio: verifique o pipeline de dados"
colunas_necessarias = [/* liste aqui as colunas que esta tarefa usa */]
colunas_ausentes = [c for c in colunas_necessarias if c not in df.columns]
assert not colunas_ausentes, f"Colunas ausentes: {colunas_ausentes}"
```

### 2b. Validar tipos e ranges
```python
# Para colunas numéricas de KPI:
assert df["coluna_kpi"].between(0, valor_maximo).all(), "Valor fora do range esperado"

# Para colunas de taxa (0 a 1):
assert taxa_calculada >= 0 and taxa_calculada <= 1, f"Taxa inválida: {taxa_calculada}"

# Para colunas categóricas:
assert df["coluna_cat"].notna().all(), "Nulos não tratados na coluna categórica"
```

### 2c. Verificar resultado do KPI antes de exibir
Calcule o KPI usando a **fórmula canônica** e imprima o valor esperado antes de conectar ao `st.metric()`:

```python
# Fórmulas canônicas — usar exatamente estas:
taxa_conversao    = len(checkins[checkins["efetuou_checkin"] == True]) / interacoes["visualizacoes_perfil"].sum()
taxa_save         = interacoes["saves_favoritos"].sum() / interacoes["visualizacoes_perfil"].sum()
taxa_compartilhar = interacoes["compartilhamentos"].sum() / interacoes["visualizacoes_perfil"].sum()
taxa_uso_promo    = promocoes["quantidade_utilizada"] / promocoes["quantidade_disponibilizada"]
taxa_retencao     = (retencao["num_checkins"] >= 2).sum() / len(retencao)

# Benchmarks para delta=:
# conversão: ≥35% | save: ≥12% | compartilhamento: ≥4%
```

---

## Princípio 3 — No Mocks (Artigo 4 da Constituição)

**Lista de proibições absolutas nesta tarefa:**

```python
# ❌ PROIBIDO — nunca escrever isso em dashboard_donos.py
df_fake = pd.DataFrame({"col": [1, 2, 3]})
taxa_conversao = 0.32          # hardcoded
st.metric("KPI", "32%")        # sem calcular do dataset
df_teste = df.head(10)         # amostra usada como dado real
valor = random.random()        # dados gerados
```

**Verificação:** Rastreie a origem de cada variável exibida ao usuário. Se o caminho não levar até `carregar_dados()` → ZIP → CSV, o dado é mock e deve ser removido.

**Única exceção permitida:** constantes de benchmark (`BENCHMARK_CONVERSAO = 0.35`) são definições de negócio, não dados simulados.

```python
# ✅ PERMITIDO — constantes de negócio
BENCHMARK_CONVERSAO    = 0.35   # ≥35% — meta da plataforma
BENCHMARK_SAVE         = 0.12   # ≥12%
BENCHMARK_COMPARTILHAR = 0.04   # ≥4%
```

---

## Princípio 4 — Sacred CI (Artigo 5 da Constituição)

**A tarefa só está done quando `streamlit run dashboard_donos.py` executa sem erros.**

### 4a. Checklist pré-commit obrigatório

Execute mentalmente (ou no terminal) antes de finalizar:

- [ ] `st.set_page_config()` continua sendo a **primeira linha executável** do arquivo
- [ ] Nenhum `import` customizado antes de `st.set_page_config()`
- [ ] `@st.cache_data` presente em todas as funções de carga (Artigo 7)
- [ ] Todo `px.*` ou `go.*` tem `if not df.empty:` imediatamente acima (Artigo 9)
- [ ] Toda exceção de carga usa o padrão `try/except + st.error() + st.stop()`
- [ ] Nenhum `exit()` ou `sys.exit()` adicionado
- [ ] Nenhum `print()` de debug com dados de usuários

### 4b. Padrão de tratamento de erros
```python
# ✅ CORRETO — padrão Sacred CI
try:
    dados = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# ✅ CORRETO — guarda de vazio (Artigo 9 — Empty-Guard)
if not df_filtrado.empty:
    fig = px.bar(df_filtrado, ...)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">💡 <strong>Insight:</strong> ...</div>', unsafe_allow_html=True)
else:
    st.info("Nenhum dado encontrado para os filtros selecionados.")
```

### 4c. Checklist de qualidade Plotly (Artigo 8 — Palette-Strict)
```python
# Todo gráfico deve ter:
fig = px.bar(
    df,
    title="Título descritivo e objetivo",           # obrigatório
    labels={"col_x": "Rótulo X", "col_y": "Rótulo Y"},  # obrigatório
    text="coluna_valor",                            # obrigatório para barras
    color_discrete_sequence=[                       # obrigatório — paleta Explori
        "#E07A2F",  # COR_PRIMARIA
        "#B96A4A",  # COR_SECUNDARIA
        "#6B7A3A",  # COR_VERDE
        "#8A9450",  # COR_NEUTRO
    ],
)
fig.update_traces(textposition="outside")           # obrigatório para barras
fig.update_layout(
    plot_bgcolor="white",                           # obrigatório
    paper_bgcolor="white",                          # obrigatório
    font=dict(color="#2D2D2D"),
)
st.plotly_chart(fig, use_container_width=True)      # obrigatório
```

---

## Formato de Entrega

Ao finalizar a implementação, produza o relatório abaixo:

```
RELATÓRIO DE EXECUÇÃO — ${input:taskId}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tarefa: ${input:taskTitulo}
Arquivo(s) modificado(s): ${input:arquivos}

PRINCÍPIOS CONSTITUCIONAIS
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Library-First   — [o que foi reutilizado da biblioteca]
✅ Test-First      — [quais asserts foram adicionados]
✅ No Mocks        — [confirmação: todos os dados vêm do dataset ZIP]
✅ Sacred CI       — [confirmação: streamlit run executou sem erros]

CRITÉRIOS DE DONE (do tasks.md)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ [critério 1] — [como foi verificado]
✅ [critério 2] — [como foi verificado]
✅ streamlit run sem erros — confirmado

PRÓXIMA TAREFA
━━━━━━━━━━━━━━
→ [TASK-NN]: [título] (depende desta tarefa — pode iniciar)
→ [TASK-MM]: [título] (ainda bloqueada por TASK-XX)
```

Se qualquer critério de done **não** foi atendido, liste como `❌` com a razão e o que falta fazer antes de marcar a tarefa como concluída.
