---
mode: ask
description: Cria uma nova tela completa no dashboard Explori com gráficos, KPIs e insights seguindo todos os padrões do projeto. Use este prompt ao adicionar uma nova página ao dashboard_donos.py.
---

Crie uma nova tela Streamlit para o dashboard Explori com as seguintes especificações:

**Nome da tela:** ${input:nomeTela:Ex: Análise de Sazonalidade}
**Ícone emoji:** ${input:icone:Ex: 📅}
**Objetivo da tela:** ${input:objetivo:O que o dono do restaurante vai aprender nesta tela?}
**Tabelas necessárias:** ${input:tabelas:Ex: checkins, usuarios, categorias}

---

## Requisitos obrigatórios

### Estrutura
- O bloco da tela deve ser adicionado como `elif pagina == "${input:icone} ${input:nomeTela}":` no bloco de navegação
- Iniciar com `st.title("${input:icone} ${input:nomeTela}")` e `st.caption()` explicando o objetivo
- Finalizar com `st.divider()` antes da próxima seção

### Dados
- Usar apenas as tabelas: **${input:tabelas}**
- Verificar `if not df.empty` antes de cada gráfico
- Nunca exibir `id_usuario` ou `id_estabelecimento` ao usuário final
- Aplicar todos os tratamentos de dados conforme o pipeline canônico da skill `data-pipeline`

### Gráficos
- Mínimo de **2 gráficos** na tela
- Usar exclusivamente a paleta Explori:
  - `COR_PRIMARIA = "#E07A2F"` (principal)
  - `COR_VERDE = "#6B7A3A"` (positivo)
  - `COR_SECUNDARIA = "#B96A4A"` (complementar)
- Todo gráfico deve ter: título, eixos nomeados, valores visíveis, `plot_bgcolor="white"`, `use_container_width=True`
- Todo gráfico deve ser seguido de uma `insight-box`

### KPIs
- Se houver cards de KPI, usar `st.columns()` + `st.metric()`
- Incluir `delta=` com o benchmark da plataforma quando aplicável:
  - Conversão: `delta="Meta: ≥35%"`
  - Save: `delta="Meta: ≥12%"`
  - Compartilhamento: `delta="Meta: ≥4%"`

### Insights
- Referenciar pelo menos **1 dos 7 insights estratégicos** confirmados pela análise exploratória
- Texto da `insight-box` em linguagem simples, acessível para donos de restaurantes sem conhecimento técnico

---

## Formato de entrega

Entregue o código Python completo do bloco `elif` da nova tela, pronto para ser inserido no `dashboard_donos.py`, respeitando a indentação e o estilo do arquivo existente.
