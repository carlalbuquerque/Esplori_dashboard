# Convenções Globais — Explori Dashboard

## Produto

A **Explori** é uma plataforma de descoberta de experiências gastronômicas e de lazer focada na Região Metropolitana do Recife (RMR) e no interior de Pernambuco. Este repositório contém o **dashboard para donos de restaurantes**: uma interface Streamlit que transforma dados de check-ins, visualizações, saves e promoções em insights acionáveis para o negócio.

---

## Tech Stack

| Camada | Tecnologia | Versão mínima |
|--------|-----------|--------------|
| Linguagem | Python | 3.10+ |
| Framework web | Streamlit | 1.32.0 |
| Gráficos | Plotly Express + Plotly Graph Objects | 5.18.0 |
| Manipulação de dados | Pandas | 2.0.0 |
| Dados | CSVs extraídos de `data/dataset_eda_ficticio.zip` | — |

Nunca introduzir dependências fora deste stack sem justificativa explícita. Matplotlib pode ser usado **somente** em scripts exploratórios fora do dashboard (`documento projeto/colab/`), nunca em arquivos do dashboard Streamlit.

---

## Estrutura do Repositório

```
.
├── .github/
│   ├── copilot-instructions.md   ← este arquivo (convenções globais)
│   ├── instructions/             ← regras específicas por tipo de arquivo
│   │   └── explori-dashboard.instructions.md  (applyTo: **/*.py)
│   ├── prompts/                  ← prompts reutilizáveis
│   ├── agents/                   ← agentes customizados
│   └── skills/                   ← skills de domínio
├── data/
│   └── dataset_eda_ficticio.zip  ← fonte de dados principal
├── documento projeto/
│   ├── colab/
│   │   └── analise_dados_esplori_2025_2026.py  ← análise exploratória (referência)
│   └── documentos/
│       ├── CONTEXTO_DASHBOARD_DONOS.md          ← contexto completo do produto
│       └── Padrão de aceitação dos graficos.docx
├── dashboard_donos.py            ← app Streamlit principal
└── requirements.txt
```

---

## Padrões de Código

### Nomenclatura
- Variáveis, funções e arquivos em **português** seguindo o padrão do projeto: `usuarios`, `checkins`, `interacoes`, `estab`, `promocoes`, `categorias`.
- Funções auxiliares com prefixo descritivo: `carregar_dados()`, `calcular_kpis()`, `plot_funil()`.
- Constantes de cor em `UPPER_SNAKE_CASE`: `COR_PRIMARIA`, `COR_VERDE`.

### Estrutura de um arquivo Streamlit neste projeto
```python
# 1. CONFIGURAÇÃO DA PÁGINA  (st.set_page_config — sempre primeiro)
# 2. PALETA DE CORES         (constantes COR_*)
# 3. CSS CUSTOMIZADO         (st.markdown com unsafe_allow_html=True)
# 4. CARGA DE DADOS          (funções com @st.cache_data)
# 5. SIDEBAR                 (navegação + filtros globais)
# 6. PÁGINAS                 (um bloco if/elif por página)
```

### Cache obrigatório
Toda função que lê arquivos ou faz transformações pesadas deve usar `@st.cache_data`:
```python
@st.cache_data
def carregar_dados():
    ...
```

### Verificação antes de plotar
Sempre checar `if not df.empty` antes de gerar qualquer gráfico para evitar erros silenciosos em produção.

### Tratamento de dados nulos
| Coluna | Tratamento padrão |
|--------|------------------|
| `genero` | `.fillna("não informado")` |
| `origem_geografica` | `.fillna(moda)` + `.str.lower().str.strip()` |
| `efetuou_checkin` | `.fillna(False).astype(bool)` |
| `criacao_promocoes` | `.fillna(0)` |
| `visualizacoes_perfil`, `saves_favoritos`, `compartilhamentos` | `.fillna(0).astype(int)` |
| `quantidade_disponibilizada` | `.fillna(mediana)` |
| `data_hora_checkin` | `pd.to_datetime(..., errors='coerce')` |
| `idade` | `dropna` + filtro `18 <= idade <= 65` |

---

## Paleta de Cores

```python
COR_PRIMARIA   = "#E07A2F"   # barras principais, destaques, CTAs
COR_SECUNDARIA = "#B96A4A"   # elementos complementares
COR_VERDE      = "#6B7A3A"   # indicadores positivos / sucesso
COR_NEUTRO     = "#8A9450"   # gráficos de apoio, terceira série
COR_FUNDO      = "#F9F5F0"   # background do dashboard
COR_TEXTO      = "#2D2D2D"   # títulos e corpo de texto
```

Todo `px.*` ou `go.*` deve ter `color_discrete_sequence` ou `color_discrete_map` mapeando para esta paleta. Nunca usar as cores padrão do Plotly.

---

## Padrão de Gráficos (Checklist obrigatório)

Antes de finalizar qualquer gráfico, verificar:

- [ ] `title=` definido com descrição clara e objetiva
- [ ] Eixos nomeados via `labels={}` ou `update_layout(xaxis_title=, yaxis_title=)`
- [ ] `text=coluna` com `textposition="outside"` para gráficos de barras
- [ ] `plot_bgcolor="white", paper_bgcolor="white"` no `update_layout`
- [ ] `st.plotly_chart(fig, use_container_width=True)`
- [ ] Caixa de insight logo abaixo do gráfico

```python
# Padrão de caixa de insight
st.markdown(
    '<div class="insight-box">💡 <strong>Insight:</strong> Texto aqui.</div>',
    unsafe_allow_html=True,
)
```

---

## KPIs e Fórmulas Canônicas

```python
taxa_conversao    = len(checkins) / interacoes["visualizacoes_perfil"].sum()
taxa_save         = interacoes["saves_favoritos"].sum() / interacoes["visualizacoes_perfil"].sum()
taxa_compartilhar = interacoes["compartilhamentos"].sum() / interacoes["visualizacoes_perfil"].sum()
taxa_uso_promo    = promocoes["quantidade_utilizada"] / promocoes["quantidade_disponibilizada"]
taxa_retencao     = (retencao["num_checkins"] >= 2).sum() / len(retencao)
```

Benchmarks da plataforma (usar como referência nos cards de KPI):
- Taxa de conversão ≥ 35%
- Taxa de save ≥ 12%
- Taxa de compartilhamento ≥ 4%

---

## Comandos do Projeto

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar o dashboard
streamlit run dashboard_donos.py

# Rodar análise exploratória (referência — não faz parte do dashboard)
# Execute no Google Colab ou Jupyter:
# documento projeto/colab/analise_dados_esplori_2025_2026.py
```

---

## O que NÃO fazer

- ❌ `matplotlib.pyplot` como visualização principal no dashboard
- ❌ Remover `@st.cache_data` das funções de carregamento
- ❌ Calcular KPIs antes de limpar os dados
- ❌ Gráfico sem título, sem eixos nomeados ou sem valor numérico visível
- ❌ Cores fora da paleta Explori sem justificativa
- ❌ Exibir colunas de IDs (`id_usuario`, `id_estabelecimento`) para o usuário final
- ❌ `st.plotly_chart(fig)` sem `use_container_width=True`
- ❌ Instalar pacotes não listados em `requirements.txt` sem atualizar o arquivo
