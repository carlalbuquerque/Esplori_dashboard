---
applyTo: "**/*.py"
---

# Instruções do Projeto — Explori Dashboard (Donos de Restaurantes)

## Visão Geral do Projeto

Este repositório contém o dashboard **Explori** voltado para donos e gerentes de restaurantes cadastrados na plataforma. O objetivo é transformar os dados da plataforma em insights acessíveis e acionáveis para apoiar decisões de negócio.

A Explori é uma plataforma de descoberta de experiências gastronômicas focada na Região Metropolitana do Recife (RMR) e no interior de Pernambuco. Os dados vêm de check-ins, visualizações de perfil, saves, compartilhamentos e promoções dos estabelecimentos.

---

## Stack Tecnológica

- **Framework web**: Streamlit (`streamlit>=1.32.0`)
- **Gráficos**: Plotly Express e Plotly Graph Objects (`plotly>=5.18.0`)
- **Dados**: Pandas (`pandas>=2.0.0`)
- **Linguagem**: Python 3.10+
- **Fonte de dados**: CSVs extraídos de `dataset_eda_ficticio.zip` na pasta `data/`

Nunca use Matplotlib como biblioteca principal de gráficos neste projeto — use sempre Plotly para garantir interatividade nos gráficos do Streamlit.

---

## Estrutura de Dados

O dataset é composto por 6 tabelas CSV. Ao manipular esses dados, respeite os nomes de colunas abaixo:

### `usuarios.csv`
- `id_usuario`, `idade` (int, 18–65), `genero` (masculino/feminino/não informado)
- `origem_geografica` (string, padronizar com `.str.lower().str.strip()`)
- `horario_maior_busca` (formato `HH:MM:SS`)
- `efetuou_checkin` (bool)

### `estabelecimentos.csv`
- `id_estabelecimento`, `nome_estabelecimento`
- `origem_geografica`, `faixa_de_gasto` (baixo/medio/alto)
- `criacao_promocoes` (int, preencher nulos com 0)

### `categorias.csv`
- `id_categoria`, `nome_categoria`

### `estabelecimento_categoria.csv`
- `id_estabelecimento`, `id_categoria`

### `checkins.csv`
- `id_checkin`, `id_usuario`, `id_estabelecimento`, `id_categoria`
- `data_hora_checkin` (converter com `pd.to_datetime(..., errors='coerce')`)
- `faixa_gasto`, `usou_voucher` (bool)

### `interacoes.csv`
- `id_usuario`, `id_estabelecimento`
- `visualizacoes_perfil`, `saves_favoritos`, `compartilhamentos` (int, preencher nulos com 0)

### `promocoes.csv`
- `id_promocao`, `id_estabelecimento`
- `quantidade_disponibilizada` (preencher nulos com a mediana)
- `quantidade_utilizada` (não pode exceder `quantidade_disponibilizada`)
- `taxa_uso` = `quantidade_utilizada / quantidade_disponibilizada` (calcular após limpeza)

---

## Paleta de Cores Obrigatória

Sempre use a identidade visual da Explori. Nunca substitua por outras paletas sem solicitação explícita.

```python
COR_PRIMARIA   = "#E07A2F"  # barras principais, destaques, CTAs
COR_SECUNDARIA = "#B96A4A"  # elementos complementares
COR_VERDE      = "#6B7A3A"  # indicadores positivos / sucesso
COR_NEUTRO     = "#8A9450"  # gráficos de apoio, terceira série
COR_FUNDO      = "#F9F5F0"  # background do dashboard
COR_TEXTO      = "#2D2D2D"  # títulos e corpo
```

---

## Padrão de Qualidade dos Gráficos

Todo gráfico gerado neste projeto deve seguir estes critérios obrigatórios:

1. **Título claro e objetivo** — descreve exatamente o que o gráfico mostra
2. **Eixos nomeados** com unidade de medida quando aplicável
3. **Valores numéricos visíveis** sobre barras, pontos ou fatias (`text=coluna`, `textposition="outside"`)
4. **Legenda presente** quando houver mais de uma série de dados
5. **Fundo branco** — sempre definir `plot_bgcolor="white", paper_bgcolor="white"` no `update_layout`
6. **Cores da paleta Explori** — nunca usar cores padrão do Plotly sem mapear para a paleta do projeto
7. **Gráfico responsivo** — sempre usar `st.plotly_chart(fig, use_container_width=True)`
8. **Insight contextual** logo abaixo de cada gráfico, em linguagem simples para leigos em dados

Exemplo de insight:
```python
st.markdown(
    '<div class="insight-box">💡 <strong>Insight:</strong> Seu texto aqui.</div>',
    unsafe_allow_html=True,
)
```

---

## Estrutura de Telas do Dashboard

O dashboard é organizado em 6 páginas navegáveis via `st.sidebar`:

| Página | Conteúdo principal |
|--------|-------------------|
| 📊 Resumo Executivo | KPIs: Visualizações, Check-ins, Saves, Taxa de Conversão |
| 👥 Perfil do Público | Faixa etária × gênero, top cidades, horário de pico |
| 🔄 Funil de Engajamento | Funil visual + comparativo com/sem check-in |
| 🏆 Ranking & Concorrência | Top 10 por check-ins e visualizações + concorrência por faixa de gasto |
| 🎟️ Promoções & Vouchers | Taxa de uso das promoções + impacto do voucher |
| 🔁 Retenção de Clientes | Frequência de retorno + recomendações de fidelização |

---

## KPIs e Fórmulas

Ao calcular métricas, use sempre as fórmulas abaixo:

```python
taxa_conversao    = len(checkins) / interacoes["visualizacoes_perfil"].sum()  # meta ≥ 35%
taxa_save         = interacoes["saves_favoritos"].sum() / interacoes["visualizacoes_perfil"].sum()  # meta ≥ 12%
taxa_compartilhar = interacoes["compartilhamentos"].sum() / interacoes["visualizacoes_perfil"].sum()  # meta ≥ 4%
taxa_uso_promo    = promocoes["quantidade_utilizada"] / promocoes["quantidade_disponibilizada"]
taxa_retencao     = (retencao["num_checkins"] >= 2).sum() / len(retencao)
```

---

## Convenções de Código

- Todas as funções de carregamento de dados devem usar `@st.cache_data` para evitar recarregamentos desnecessários.
- Tratar dados ausentes **antes** de calcular qualquer KPI ou gráfico.
- Usar `observed=False` em `groupby` com colunas categóricas (`pd.Categorical`).
- Verificar `if not df.empty` antes de plotar qualquer gráfico para evitar erros silenciosos.
- Nomes de variáveis e funções em português (seguindo o padrão do projeto): `usuarios`, `checkins`, `interacoes`, `estab`, `promocoes`, `categorias`.
- Comentários de seção com o padrão: `# ─── Descrição ─────────────────────────────`

---

## Insights Estratégicos (Referenciar no Código)

Estes insights devem aparecer como caixas contextuais no dashboard. Use-os como base ao gerar recomendações:

- **Horário de pico 13h–16h** — publicar promoções às 12h30 maximiza o alcance
- **~84% dos usuários fazem 1 único check-in** — maior oportunidade de retenção do projeto
- **Recife concentra ~46% dos usuários** — campanhas fora da RMR devem ser segmentadas
- **Saves antecedem check-ins** — usuários que salvam têm maior probabilidade de conversão
- **Maioria das promoções não atinge 100% de uso** — revisar mecânica e comunicação
- **Faixa "baixo" domina** — restaurantes de ticket alto devem diferenciação por experiência
- **Funil clássico**: visualizações >> saves >> compartilhamentos >> check-ins

---

## O que NÃO fazer

- ❌ Não usar `matplotlib.pyplot` como biblioteca de visualização principal
- ❌ Não remover o `@st.cache_data` das funções de carregamento de dados
- ❌ Não calcular KPIs sem antes limpar os dados (nulos, duplicatas, faixas inválidas de idade)
- ❌ Não criar gráficos sem título, sem eixos nomeados ou sem valor numérico visível
- ❌ Não usar cores fora da paleta Explori sem justificativa explícita
- ❌ Não expor colunas de IDs (`id_usuario`, `id_estabelecimento`) em tabelas para o usuário final
- ❌ Não ignorar o `use_container_width=True` no `st.plotly_chart`
