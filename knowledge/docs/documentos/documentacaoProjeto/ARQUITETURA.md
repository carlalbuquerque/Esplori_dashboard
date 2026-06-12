# Arquitetura do Projeto — Explori Dashboard
# Arquitetura de Código — Explori Dashboard

**Objetivo:** documento enxuto e focado exclusivamente na organização e contratos do código fonte, pontos de extensão, fluxo de dados no código e responsabilidades de módulos.

**Versão:** 1.1 | **Data:** 2026-06-12

---

## Visão geral (apenas código)

- Entrada do app: `app.py` ou `dashboard_donos.py` — contêm a configuração da página (`st.set_page_config`), carregam CSS e roteiam para os módulos de view via `render(dados, kpis)`.
- Funções de carga e processamento: `utils/dados.py` (função pública `carregar_dados()` e `calcular_kpis()`).
- Constantes e temas: `utils/constantes.py` (cores, benchmarks, `CSS_CUSTOMIZADO`).
- Views (cada tela é um módulo com `render(dados, kpis)`): `views/perfil_publico.py`, `views/engajamento.py`, `views/retencao.py`, `views/promocoes.py`, `views/benchmarking.py`.

## Módulos e responsabilidades

- `app.py` / `dashboard_donos.py`:
        - Inicializa sessão Streamlit e `st.session_state` para `pagina`.
        - Monta `sidebar` com navegação e filtros globais.
        - Chama `_PAGINAS[pagina].render(dados, kpis)`.

- `utils/dados.py`:
        - `carregar_dados()` — procura ZIP em `data/`, extrai para `data/extracted/` (protegendo contra path traversal), lê CSVs e faz limpeza (idade, gênero, tipos, duplicatas). Marcada com `@st.cache_data`.
        - `calcular_kpis(checkins, interacoes, promocoes)` — retorna dicionário com métricas usadas pelas views.

- `utils/constantes.py`:
        - Declara paleta, benchmarks canônicos e `CSS_CUSTOMIZADO` usado pelo app.

- `views/*.py`:
        - Cada arquivo exporta `render(dados: tuple, kpis: dict) -> None`.
        - Responsabilidade de cada view: filtrar dados necessários, construir gráficos Plotly (px/go), exibir `st.metric()` e `insight-box` com `st.markdown(..., unsafe_allow_html=True)`.

## Contratos entre módulos

- `carregar_dados()` → retorna tuple: `(usuarios, estab, categorias, estab_cat, checkins, interacoes, promocoes)`.
- `calcular_kpis(checkins, interacoes, promocoes)` → dicionário com chaves: `total_views`, `total_saves`, `total_shares`, `total_checkins`, `taxa_conversao`, `taxa_save`, `taxa_compartilhar`, `taxa_retencao`, `taxa_uso_promo`, `retencao`.
- `render(dados, kpis)` nos `views` espera a tupla de dataframes e o dicionário de KPIs.

## Fluxo de dados (no código)

1. `app.py` chama `carregar_dados()`.
2. `carregar_dados()` extrai/ler CSVs, limpa e retorna os DataFrames.
3. `app.py` chama `calcular_kpis()` e obtém `kpis`.
4. `app.py` roteia para o `render()` da view ativa, passando `dados` e `kpis`.
5. Views fazem merges/aggregations locais conforme necessário e exibem gráficos.

## Padrões e boas práticas observadas

- Views são idempotentes: recebem dados limpos e não alteram a fonte.
- Uso consistente de `@st.cache_data` para evitar recálculo caro.
- Uso consolidado de `utils/constantes.py` para paleta e benchmarks — facilita mudanças globais.
- Gráficos sempre atualizam layout com `plot_bgcolor`/`paper_bgcolor` e `font=dict(color=...)`.

## Pontos de extensão e melhorias (rápidas)

- Extrair um `router` simples para evitar duplicação entre `app.py` e `dashboard_donos.py`.
- Encapsular cálculos de métricas por entidade em `utils/metrics.py` para facilitar testes unitários.
- Adicionar typing mais estrito (`TypedDict` para `kpis`, `Protocol` para views) para melhorar legibilidade e testes.

---

Arquivo focado em código pronto — se quiser, aplico tipagens e extraio `utils/metrics.py` agora.
```
REQUISITO DE NEGÓCIO
        │
        ▼ /requisito-para-spec
SPEC.MD (user stories + AC + marcadores de incerteza)
        │
        ▼ /spec-para-plano
PACOTE DE PLANEJAMENTO
  ├── plan.md       (fases e tarefas)
  ├── data-model.md (schema específico)
  ├── contracts/    (contratos de componentes)
  ├── research.md   (insights aplicáveis)
  └── quickstart.md (guia de validação)
        │
        ▼ /plano-para-tarefas
TASKS.MD (tarefas atômicas + grafo de dependências + critérios de done)
        │
        ▼ /executar-tarefa (×N, uma TASK por vez)
IMPLEMENTAÇÃO (@dashboard-builder)
  Princípio 1: Library-First
  Princípio 2: Test-First
  Princípio 3: No Mocks
  Princípio 4: Sacred CI
        │
        ▼ /revisar-codigo (@security-reviewer)
REVISÃO DE SEGURANÇA + QUALIDADE
        │
        ▼
ENTREGA — streamlit run dashboard_donos.py ✅
```

---

## 10. Decisões de Arquitetura e Justificativas

| Decisão | Alternativa rejeitada | Justificativa |
|---------|----------------------|---------------|
| Arquivo único (`dashboard_donos.py`) | Multi-arquivo com módulos | Projeto de escopo bem definido; overhead de modularização não justificado |
| ZIP local como fonte de dados | Banco de dados / API | Projeto acadêmico/demonstração; sem requisito de atualização em tempo real |
| Streamlit puro | Dash / FastAPI + React | Velocidade de desenvolvimento; público-alvo familiar com Streamlit |
| `@st.cache_data` | Sem cache | Dataset ~33k registros; recalcular a cada interação tornaria o app lento |
| Plotly (não Matplotlib) | Matplotlib | Gráficos interativos nativos no Streamlit; API mais expressiva para Pandas |
| Português nos identificadores | Inglês | Alinhamento com convenções da equipe e documentação do produto |
| ZIP com proteção path traversal | Descompactar o ZIP | Segurança; evitar arquivos maliciosos sobrescreverem o sistema |

---

*Arquitetura definida para o Explori Dashboard — plataforma de insights para donos de restaurantes na RMR.*
