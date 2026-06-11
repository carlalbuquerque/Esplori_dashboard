# Constituição do Projeto — Explori Dashboard

> **Status:** Vigente | **Versão:** 1.0 | **Data:** 2026-06-11  
> Estas regras são invioláveis. Qualquer desvio exige justificativa explícita registrada em comentário no commit.

---

## Artigo 1 — Library-First (Biblioteca Prioritária)

**Regra:** Usar sempre a stack aprovada antes de escrever qualquer código customizado. Se Streamlit, Plotly ou Pandas já resolve, não se escreve do zero.

**Manifestações proibidas:**
- Implementar sistema de layout próprio quando `st.columns()` atende
- Criar funções de formatação de número quando `f"{valor:.1%}"` existe
- Usar `matplotlib` no dashboard quando `px.*` ou `go.*` resolve o mesmo problema
- Instalar pacotes não listados em `requirements.txt` sem atualizar o arquivo

**Stack aprovada e imutável:**

| Biblioteca | Versão mínima | Uso |
|-----------|--------------|-----|
| `streamlit` | 1.32.0 | Framework web |
| `plotly` | 5.18.0 | Todos os gráficos |
| `pandas` | 2.0.0 | Manipulação de dados |
| `openpyxl` | — | Leitura de Excel (se necessário) |

> `matplotlib` é permitido **exclusivamente** em scripts exploratórios dentro de `documento projeto/colab/`. Nunca em arquivos do dashboard.

---

## Artigo 2 — CLI Mandate (Mandato CLI)

**Regra:** O projeto inteiro deve ser instalado e executado com exatamente dois comandos. Qualquer processo que não seja reproduzível via CLI é inválido.

**Os dois comandos canônicos:**
```bash
pip install -r requirements.txt
streamlit run dashboard_donos.py
```

**Implicações:**
- Toda dependência nova vai para `requirements.txt` com versão fixada (`pacote==X.Y.Z`)
- Nenhum passo de configuração manual é aceitável (sem "antes, edite o arquivo X", sem credenciais hardcoded)
- Caminhos de arquivo são sempre relativos ao `cwd` do projeto, nunca absolutos
- Variáveis de ambiente sensíveis (se algum dia necessárias) usam `.env` com `python-dotenv`

**Verificação:** Um desenvolvedor novo deve rodar o projeto em menos de 5 minutos a partir do clone do repositório.

---

## Artigo 3 — Test-First (Validação Antes de Plotar)

**Regra:** Nenhum gráfico é implementado antes de validar que os dados de entrada estão limpos e que o resultado esperado é conhecido.

**Protocolo obrigatório antes de criar qualquer visualização:**

```python
# 1. Verificar shape e tipos
assert not df.empty, "DataFrame vazio antes do plot"
assert "coluna_esperada" in df.columns

# 2. Verificar range dos valores
assert df["taxa_conversao"].between(0, 1).all(), "Taxa fora do range 0-1"

# 3. Verificar ausência de nulos nas colunas plotadas
assert df["coluna_x"].notna().all()
```

**Para KPIs, registrar o valor esperado antes de calcular:**

| KPI | Range esperado | Benchmark |
|-----|---------------|-----------|
| Taxa de conversão | 0% – 100% | ≥ 35% |
| Taxa de save | 0% – 100% | ≥ 12% |
| Taxa de compartilhamento | 0% – 100% | ≥ 4% |
| Taxa de uso de promoção | 0% – 100% | ≥ 50% |
| Taxa de retenção | 0% – 100% | > 16% (acima de 1 check-in) |

> Gráfico sem validação prévia dos dados é gráfico que falha silenciosamente em produção.

---

## Artigo 4 — No Mocks (Sem Dados Simulados)

**Regra:** O dashboard usa exclusivamente os dados reais extraídos do arquivo `data/dataset_eda_ficticio.zip`. Nenhum DataFrame artificial, valor hardcoded de KPI ou dado simulado é permitido no código de produção.

**Proibido em `dashboard_donos.py`:**
```python
# ❌ PROIBIDO — dados simulados
df_fake = pd.DataFrame({"checkins": [100, 200, 300]})
taxa_conversao = 0.32  # valor hardcoded

# ❌ PROIBIDO — placeholder antes de conectar dados reais
st.metric("Conversão", "32%")  # sem calcular do dataset
```

**Permitido apenas em:**
- Scripts de análise exploratória em `documento projeto/colab/`
- Testes unitários isolados (se criados futuramente em `tests/`)

**Exceção controlada:** Valores de benchmark da plataforma (`≥35%`, `≥12%`, `≥4%`) podem ser constantes, pois são definições de negócio, não dados medidos.

---

## Artigo 5 — Sacred CI (Execução Sagrada)

**Regra:** O comando `streamlit run dashboard_donos.py` deve sempre executar sem erros ou warnings críticos. Este é o único "teste de integração" do projeto — e é sagrado.

**O que "executar sem erros" significa:**
- Nenhum `Exception` não tratado no startup
- Sidebar renderiza corretamente
- Pelo menos a página inicial carrega sem tela em branco
- Nenhum `DeprecationWarning` do Streamlit sobre APIs removidas

**Regras derivadas:**
- `st.set_page_config()` é sempre a **primeira linha executável** do arquivo, antes de qualquer import customizado
- Toda exceção de carregamento de dados usa o padrão:
  ```python
  try:
      dados = carregar_dados()
  except Exception as e:
      st.error(f"Erro ao carregar dados: {e}")
      st.stop()
  ```
- `st.stop()` é preferível a deixar o app em estado indefinido
- Nunca usar `exit()` ou `sys.exit()` — interrompe o servidor Streamlit

**Gate de qualidade:** Antes de qualquer commit, executar manualmente `streamlit run dashboard_donos.py` e navegar por todas as páginas.

---

## Artigo 6 — Portuguese-First (Código em Português)

**Regra:** Todos os identificadores de código — variáveis, funções, parâmetros, colunas derivadas, constantes — são escritos em português. Inglês é reservado para nomes de bibliotecas, APIs externas e palavras-chave da linguagem.

**Tabela de referência — nomes canônicos:**

| Conceito | Nome correto | Nome proibido |
|---------|-------------|--------------|
| DataFrame de usuários | `usuarios` | `users`, `df_users` |
| DataFrame de check-ins | `checkins` | `checkins_df`, `check_ins` |
| DataFrame de interações | `interacoes` | `interactions` |
| DataFrame de promoções | `promocoes` | `promos`, `promotions` |
| DataFrame de categorias | `categorias` | `categories` |
| Estabelecimento | `estab` | `restaurant`, `place` |
| Taxa de conversão | `taxa_conversao` | `conversion_rate` |
| Taxa de retenção | `taxa_retencao` | `retention_rate` |
| Faixa etária | `faixa_etaria` | `age_group` |
| Carregar dados | `carregar_dados()` | `load_data()` |
| Calcular KPIs | `calcular_kpis()` | `calculate_kpis()` |

**Prefixos obrigatórios por tipo:**

| Tipo | Prefixo | Exemplo |
|------|---------|---------|
| Função de carregamento | `carregar_` | `carregar_dados()` |
| Função de cálculo | `calcular_` | `calcular_kpis()` |
| Função de plot | `plot_` | `plot_funil()` |
| Constante de cor | `COR_` | `COR_PRIMARIA` |
| Constante de path | `PATH_` | `PATH_DADOS` |

---

## Artigo 7 — Cache-Always (Cache Obrigatório)

**Regra:** Toda função que lê arquivos, faz transformações pesadas ou executa cálculos de KPIs sobre o dataset completo deve usar `@st.cache_data`. Cache nunca é removido sem justificativa de performance documentada em comentário.

**Padrão obrigatório:**
```python
@st.cache_data
def carregar_dados() -> dict[str, pd.DataFrame]:
    """Carrega e limpa todos os CSVs do dataset Explori."""
    ...
    return {"usuarios": usuarios, "checkins": checkins, ...}
```

**O que deve ter `@st.cache_data`:**
- Toda função que abre o ZIP e lê CSVs
- Funções que calculam métricas agregadas sobre o dataset completo
- Funções que fazem merges pesados entre tabelas

**O que NÃO deve ter `@st.cache_data`:**
- Funções que recebem filtros dinâmicos como parâmetro (o cache invalida automaticamente por parâmetro — isso é seguro, mas verificar se os parâmetros são hashable)
- Funções que chamam `st.*` internamente (gera `CachedStFunctionWarning`)
- Funções que retornam objetos não-serializáveis

**Tempo de vida:** O cache persiste durante a sessão do servidor. Para forçar recarregamento: `st.cache_data.clear()`.

---

## Artigo 8 — Palette-Strict (Paleta Inviolável)

**Regra:** Apenas as 6 cores da paleta Explori são permitidas em visualizações. As cores padrão do Plotly (`#636EFA`, `#EF553B`, etc.) são absolutamente proibidas.

**Paleta canônica — constantes imutáveis:**

```python
COR_PRIMARIA   = "#E07A2F"   # barras principais, CTAs, destaques
COR_SECUNDARIA = "#B96A4A"   # segunda série, elementos complementares
COR_VERDE      = "#6B7A3A"   # indicadores positivos, sucesso, metas atingidas
COR_NEUTRO     = "#8A9450"   # terceira série, gráficos de apoio
COR_FUNDO      = "#F9F5F0"   # background do dashboard
COR_TEXTO      = "#2D2D2D"   # títulos e corpo de texto
```

**Aplicação por tipo de gráfico:**

| Tipo | Parâmetro | Valor |
|------|-----------|-------|
| Barra única | `color_discrete_sequence` | `[COR_PRIMARIA]` |
| Duas séries | `color_discrete_sequence` | `[COR_PRIMARIA, COR_SECUNDARIA]` |
| Três séries | `color_discrete_sequence` | `[COR_PRIMARIA, COR_SECUNDARIA, COR_VERDE]` |
| Mapa de categorias | `color_discrete_map` | `{"cat_a": COR_PRIMARIA, "cat_b": COR_SECUNDARIA}` |
| Indicador positivo | direto | `COR_VERDE` |
| Funil | `marker_color` lista | `[COR_PRIMARIA, COR_SECUNDARIA, COR_VERDE, COR_NEUTRO]` |

**Obrigatório em todo `update_layout`:**
```python
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color=COR_TEXTO),
)
```

---

## Artigo 9 — Empty-Guard (Guarda de Vazio)

**Regra:** `if not df.empty:` é obrigatório imediatamente antes de qualquer chamada de gráfico ou cálculo de KPI que dependa de um DataFrame. Código sem guarda é código que quebra silenciosamente em produção.

**Padrão obrigatório:**
```python
# ✅ CORRETO
if not df_filtrado.empty:
    fig = px.bar(df_filtrado, ...)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum dado encontrado para os filtros selecionados.")
```

**Padrão proibido:**
```python
# ❌ PROIBIDO — sem guarda
fig = px.bar(df_filtrado, ...)
st.plotly_chart(fig, use_container_width=True)
```

**Onde a guarda é obrigatória:**
1. Antes de todo `px.*` ou `go.*`
2. Antes de `df["coluna"].mean()`, `.sum()`, `.max()` em DataFrames filtrados pelo usuário
3. Antes de `df.groupby(...).agg(...)` onde o grupo pode ser vazio após filtro
4. Antes de `df.iloc[0]` ou qualquer acesso por índice

**Mensagem padrão para DataFrame vazio:**
```python
st.info("Nenhum dado encontrado para os filtros selecionados. Tente ampliar o período ou remover filtros.")
```

---

## Resumo das 9 Regras

| # | Regra | Princípio Central |
|---|-------|------------------|
| 1 | Library-First | Use a stack aprovada; não reinvente |
| 2 | CLI Mandate | 2 comandos = projeto rodando do zero |
| 3 | Test-First | Valide os dados antes de plotar |
| 4 | No Mocks | Apenas dados reais do dataset ZIP |
| 5 | Sacred CI | `streamlit run` nunca pode quebrar |
| 6 | Portuguese-First | Identificadores sempre em português |
| 7 | Cache-Always | `@st.cache_data` em toda leitura pesada |
| 8 | Palette-Strict | Apenas as 6 cores Explori |
| 9 | Empty-Guard | `if not df.empty` antes de todo gráfico |

---

*Constituição definida para o projeto Explori Dashboard — dashboard para donos de restaurantes na Região Metropolitana do Recife.*
