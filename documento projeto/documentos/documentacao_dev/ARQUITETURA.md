# Arquitetura do Projeto — Explori Dashboard

> **Versão:** 1.0 | **Data:** 2026-06-11  
> Documento de referência de arquitetura para o dashboard Explori destinado a donos de restaurantes.

---

## 1. Visão Geral

```
┌─────────────────────────────────────────────────────────────────────┐
│                        EXPLORI DASHBOARD                            │
│              Dashboard para Donos de Restaurantes                   │
│                    Região Metropolitana do Recife                   │
└─────────────────────────────────────────────────────────────────────┘
         │
         │  streamlit run dashboard_donos.py
         ▼
┌────────────────────┐     ┌────────────────────┐
│   CAMADA DE        │     │   CAMADA DE         │
│   APRESENTAÇÃO     │◄────│   DADOS             │
│   (Streamlit UI)   │     │   (Pandas + ZIP)    │
└────────────────────┘     └────────────────────┘
         │                          │
         ▼                          ▼
┌────────────────────┐     ┌────────────────────┐
│   CAMADA DE        │     │   CAMADA DE         │
│   VISUALIZAÇÃO     │     │   PIPELINE          │
│   (Plotly)         │     │   (Tratamento)      │
└────────────────────┘     └────────────────────┘
```

---

## 2. Stack Tecnológica

```
┌──────────────────────────────────────────────────────────┐
│  RUNTIME                                                  │
│  Python 3.10+                                            │
├──────────────────────────────────────────────────────────┤
│  FRAMEWORK WEB          │  VISUALIZAÇÃO                  │
│  Streamlit ≥ 1.32.0     │  Plotly Express ≥ 5.18.0      │
│                         │  Plotly Graph Objects           │
├──────────────────────────────────────────────────────────┤
│  MANIPULAÇÃO DE DADOS   │  ARMAZENAMENTO                 │
│  Pandas ≥ 2.0.0         │  CSV dentro de ZIP local       │
├──────────────────────────────────────────────────────────┤
│  PROIBIDO NO DASHBOARD                                   │
│  ❌ matplotlib   ❌ banco de dados   ❌ APIs externas    │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Estrutura de Arquivos

```
Explori_dashboard/
│
├── dashboard_donos.py              ← Entrypoint único da aplicação
├── requirements.txt                ← Dependências fixadas com versão
├── README.md
│
├── data/
│   └── dataset_eda_ficticio.zip   ← Fonte de dados — NUNCA descompactar
│       ├── usuarios.csv            (~5.673 registros pós-limpeza)
│       ├── estabelecimentos.csv
│       ├── categorias.csv
│       ├── estabelecimento_categoria.csv
│       ├── checkins.csv            (~8.000+ registros válidos)
│       ├── interacoes.csv          (~20.002 registros)
│       └── promocoes.csv
│
├── documento projeto/
│   ├── colab/
│   │   └── analise_dados_esplori_2025_2026.py   ← Análise exploratória (referência)
│   └── documentos/
│       ├── ARQUITETURA.md                        ← Este arquivo
│       ├── CONSTITUICAO_PROJETO.md               ← 9 regras invioláveis
│       ├── CONTEXTO_DASHBOARD_DONOS.md           ← Contexto completo do produto
│       └── specs/                                ← Specs geradas via prompt
│
└── .github/
    ├── copilot-instructions.md      ← Convenções globais (carregadas automaticamente)
    ├── instructions/
    │   └── explori-dashboard.instructions.md    (applyTo: **/*.py)
    ├── agents/
    │   ├── dashboard-builder.agent.md
    │   ├── data-analyst.agent.md
    │   └── security-reviewer.agent.md
    ├── skills/
    │   ├── dataset-schema.md        (alwaysApply: true)
    │   ├── insights-estrategicos.md (alwaysApply: true)
    │   ├── plotly-patterns.md       (applyTo: **/*.py)
    │   └── data-pipeline.md         (applyTo: **/*.py)
    └── prompts/
        ├── nova-tela-dashboard.prompt.md
        ├── gerar-insight-kpi.prompt.md
        ├── revisar-codigo.prompt.md
        ├── converter-matplotlib-plotly.prompt.md
        ├── diagnosticar-erro.prompt.md
        ├── requisito-para-spec.prompt.md
        ├── spec-para-plano.prompt.md
        ├── plano-para-tarefas.prompt.md
        └── executar-tarefa.prompt.md
```

---

## 4. Arquitetura do `dashboard_donos.py`

O arquivo principal segue uma **estrutura linear de 6 seções obrigatórias**, sempre na mesma ordem:

```
dashboard_donos.py
│
├── SEÇÃO 1 — CONFIGURAÇÃO DA PÁGINA
│   └── st.set_page_config(...)        ← SEMPRE a primeira linha executável
│
├── SEÇÃO 2 — PALETA DE CORES
│   ├── COR_PRIMARIA   = "#E07A2F"
│   ├── COR_SECUNDARIA = "#B96A4A"
│   ├── COR_VERDE      = "#6B7A3A"
│   ├── COR_NEUTRO     = "#8A9450"
│   ├── COR_FUNDO      = "#F9F5F0"
│   └── COR_TEXTO      = "#2D2D2D"
│
├── SEÇÃO 3 — CSS CUSTOMIZADO
│   └── st.markdown(<style>...</style>, unsafe_allow_html=True)
│
├── SEÇÃO 4 — CARGA DE DADOS
│   └── @st.cache_data
│       def carregar_dados() -> dict[str, pd.DataFrame]
│           EXTRACT  → abrir ZIP (com proteção path traversal)
│           CLEAN    → tratar nulos, tipos, duplicatas
│           VALIDATE → asserts de range e completude
│           DERIVE   → faixa_etaria, hora, taxa_uso
│           RETURN   → dict com todos os DataFrames prontos
│
├── SEÇÃO 5 — SIDEBAR (Navegação + Filtros globais)
│   ├── Logo / nome do produto
│   ├── st.radio / st.selectbox → variável `pagina`
│   └── Filtros globais (período, categoria, faixa de gasto)
│
└── SEÇÃO 6 — PÁGINAS (um bloco if/elif por página)
    ├── if pagina == "🏠 Visão Geral":
    ├── elif pagina == "👥 Perfil do Público":
    ├── elif pagina == "📈 Engajamento":
    ├── elif pagina == "🔄 Retenção":
    ├── elif pagina == "🎯 Promoções":
    └── elif pagina == "🏆 Benchmarking":
```

---

## 5. Modelo de Dados

### 5.1 Diagrama Entidade-Relacionamento

```
usuarios
├── id_usuario (PK)
├── idade
├── genero
├── origem_geografica
├── horario_maior_busca
└── efetuou_checkin
        │
        │ 1:N
        ▼
checkins                    estabelecimentos
├── id_checkin (PK)         ├── id_estabelecimento (PK)
├── id_usuario (FK) ────────┤  ├── nome_estabelecimento
├── id_estabelecimento (FK)─┘  ├── origem_geografica
├── id_categoria (FK)──────┐   ├── faixa_de_gasto
├── data_hora_checkin       │   └── criacao_promocoes
├── faixa_gasto             │           │
└── usou_voucher            │           │ 1:N
                            │           ▼
interacoes                  │   promocoes
├── id_usuario (FK)         │   ├── id_promocao (PK)
├── id_estabelecimento (FK) │   ├── id_estabelecimento (FK)
├── visualizacoes_perfil    │   ├── tipo_promocao
├── saves_favoritos         │   ├── quantidade_disponibilizada
├── compartilhamentos       │   └── quantidade_utilizada
└── data_hora_interacao     │
                            ▼
                        categorias
                        ├── id_categoria (PK)
                        └── nome_categoria
                                │
                        estabelecimento_categoria
                        ├── id_estabelecimento (FK)
                        └── id_categoria (FK)
```

### 5.2 Volumes de Dados (pós-limpeza)

| Tabela | Linhas esperadas | Observação |
|--------|-----------------|-----------|
| `usuarios` | ~5.673 | Após `dropna()` em `idade` + filtro 18-65 |
| `estabelecimentos` | ~N/A | Todos os cadastrados na plataforma |
| `checkins` | ~8.000+ | Apenas `efetuou_checkin == True` |
| `interacoes` | ~20.002 | Após `.fillna(0)` nas métricas |
| `promocoes` | ~N/A | Dataset completo |

---

## 6. Fluxo de Dados

```
data/dataset_eda_ficticio.zip
         │
         │ zipfile.ZipFile (read-only, path traversal protegido)
         ▼
  pd.read_csv() × 6 tabelas
         │
         ▼
  ┌─────────────────────────────────────────┐
  │  PIPELINE DE LIMPEZA (@st.cache_data)   │
  │                                         │
  │  1. EXTRACT  — ler CSVs do ZIP          │
  │  2. CLEAN    — nulos, tipos, dupes      │
  │  3. VALIDATE — asserts de qualidade     │
  │  4. DERIVE   — colunas calculadas       │
  │  5. RETURN   — dict de DataFrames       │
  └─────────────────────────────────────────┘
         │
         │ dict["usuarios"], dict["checkins"], ...
         ▼
  ┌─────────────────────────────────────────┐
  │  CÁLCULO DE KPIs (por página)           │
  │                                         │
  │  taxa_conversao = checkins / views      │
  │  taxa_save = saves / views              │
  │  taxa_retencao = (≥2 checkins) / total  │
  │  taxa_uso_promo = util / disp           │
  └─────────────────────────────────────────┘
         │
         ▼
  ┌─────────────────────────────────────────┐
  │  RENDERIZAÇÃO (Streamlit + Plotly)      │
  │                                         │
  │  st.metric()  → cards de KPI           │
  │  px.*() / go.*() → gráficos            │
  │  insight-box  → análise contextual     │
  └─────────────────────────────────────────┘
```

---

## 7. Páginas do Dashboard

| # | Página | Ícone | Tabelas Principais | KPIs-chave |
|---|--------|-------|--------------------|-----------|
| 1 | Visão Geral | 🏠 | todas | conversão, save, retenção, promo |
| 2 | Perfil do Público | 👥 | usuarios | faixa etária, gênero, origem, horário |
| 3 | Engajamento | 📈 | interacoes, checkins | funil, taxa conversão, taxa save |
| 4 | Retenção | 🔄 | checkins, usuarios | % 1 visita, recorrentes, fiéis |
| 5 | Promoções | 🎯 | promocoes, checkins | taxa uso, impacto voucher |
| 6 | Benchmarking | 🏆 | todas | comparativo plataforma |

---

## 8. Sistema Copilot (`.github/`)

O projeto usa GitHub Copilot com configuração em 5 camadas:

```
CAMADA 1 — copilot-instructions.md
  Regras globais carregadas automaticamente em todo contexto.
  Paleta, stack, nomenclatura, KPIs canônicos.
        │
        ▼
CAMADA 2 — instructions/explori-dashboard.instructions.md
  Regras específicas para arquivos *.py.
  Schema completo, estrutura Streamlit, padrões de gráfico.
        │
        ▼
CAMADA 3 — agents/ (3 agentes especializados)
  @dashboard-builder → constrói telas e gráficos
  @data-analyst      → analisa KPIs e gera insights
  @security-reviewer → verifica LGPD e segurança
        │
        ▼
CAMADA 4 — skills/ (4 skills com conhecimento de domínio)
  dataset-schema.md      (alwaysApply) → schema das 6 tabelas
  insights-estrategicos.md (alwaysApply) → 7 insights confirmados
  plotly-patterns.md     (*.py) → templates de gráficos
  data-pipeline.md       (*.py) → pipeline canônico
        │
        ▼
CAMADA 5 — prompts/ (9 prompt templates com variáveis)
  Fluxo de desenvolvimento:
  requisito-para-spec → spec-para-plano → plano-para-tarefas → executar-tarefa
  Utilitários:
  nova-tela-dashboard | gerar-insight-kpi | revisar-codigo
  converter-matplotlib-plotly | diagnosticar-erro
```

---

## 9. Fluxo de Desenvolvimento (Workflow Completo)

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
