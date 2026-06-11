# Contexto do Dashboard Explori — Visão para Donos de Restaurantes

## 1. Visão Geral do Produto

A **Explori** é uma plataforma de descoberta de experiências gastronômicas e de lazer focada inicialmente na Região Metropolitana do Recife (RMR) e no interior de Pernambuco. O produto conecta usuários a estabelecimentos (restaurantes, bares, casas de show, etc.) por meio de check-ins, visualizações de perfil, saves e compartilhamentos.

Este dashboard tem como objetivo tornar os dados da plataforma **acessíveis e acionáveis** para donos de restaurantes, permitindo que tomem decisões mais rápidas e embasadas sobre seu negócio.

---

## 2. Público-Alvo do Dashboard

| Perfil | Descrição |
|--------|-----------|
| **Usuário primário** | Dono ou gerente de restaurante cadastrado na Explori |
| **Nível técnico** | Baixo a médio — não necessita de conhecimento em dados |
| **Frequência de uso** | Semanal ou quinzenal |
| **Dispositivo** | Desktop (prioridade) e mobile (responsividade desejável) |

---

## 3. Problema que o Dashboard Resolve

Restaurantes cadastrados na Explori não possuem visibilidade clara sobre:

- **Quem é o público** que os visualiza e faz check-in
- **Quando** os usuários estão mais ativos na plataforma
- **Como** seu estabelecimento se posiciona frente à concorrência
- **Qual o impacto real** de promoções e vouchers no engajamento
- **Quantos clientes retornam** após o primeiro check-in

---

## 4. Base de Dados Disponível

As tabelas abaixo foram analisadas e sustentam todos os indicadores do dashboard:

| Tabela | Campos-chave | Uso no Dashboard |
|--------|-------------|-----------------|
| `usuarios` | id, idade, genero, origem_geografica, horario_maior_busca, efetuou_checkin | Perfil do público, horários de pico |
| `estabelecimentos` | id, nome, origem_geografica, faixa_de_gasto, criacao_promocoes | Benchmarking, concorrência |
| `categorias` | id, nome_categoria | Análise por segmento |
| `checkins` | id, id_usuario, id_estabelecimento, id_categoria, data_hora, faixa_gasto, usou_voucher | Conversão, retenção, vouchers |
| `interacoes` | id_usuario, id_estabelecimento, visualizacoes_perfil, saves_favoritos, compartilhamentos | Funil de engajamento |
| `promocoes` | id, id_estabelecimento, quantidade_disponibilizada, quantidade_utilizada | Eficácia de promoções |

---

## 5. Indicadores-Chave (KPIs)

### 5.1 Perfil do Público (Quem visita seu restaurante)
| KPI | Descrição | Fonte |
|-----|-----------|-------|
| Faixa etária predominante | Distribuição de usuários por faixa 18-25, 26-35, 36-45, 46-55, 56-65 | `usuarios.idade` |
| Split de gênero | % Masculino / Feminino / Não informado | `usuarios.genero` |
| Top cidades de origem | Ranking das cidades com mais usuários que visitaram | `usuarios.origem_geografica` |
| Horário de pico de busca | Hora do dia com maior atividade dos usuários | `usuarios.horario_maior_busca` |

### 5.2 Engajamento & Conversão (Funil)
| KPI | Fórmula | Meta de referência |
|-----|---------|-------------------|
| Taxa de conversão (view → check-in) | check-ins / visualizações de perfil | ≥ 35% (benchmark plataforma) |
| Taxa de save (interesse) | saves / visualizações de perfil | ≥ 12% |
| Taxa de compartilhamento | compartilhamentos / visualizações de perfil | ≥ 4% |
| Drop-off do funil | usuários que visualizaram mas não converteram | — |

### 5.3 Retenção de Clientes
| KPI | Descrição |
|-----|-----------|
| Usuários com 1 check-in | % de visitantes únicos (maioria: ~84% na plataforma) |
| Usuários recorrentes (2+ check-ins) | Clientes que voltaram |
| Clientes fiéis (3+ check-ins) | Perfil altamente engajado (~1.66% na plataforma) |

### 5.4 Desempenho de Promoções
| KPI | Fórmula |
|-----|---------|
| Taxa de uso da promoção | quantidade_utilizada / quantidade_disponibilizada |
| Impacto do voucher no check-in | % de check-ins com voucher vs sem voucher |
| Promoções com baixo desempenho | taxa_uso < 30% |

### 5.5 Benchmarking Competitivo
| KPI | Descrição |
|-----|-----------|
| Posição no ranking de check-ins | Posição do restaurante vs top 10 da categoria |
| Posição no ranking de visualizações | Visibilidade relativa na plataforma |
| Média de faixa de gasto da categoria | Comparativo de preços com concorrentes |

---

## 6. Estrutura de Telas do Dashboard

```
┌─────────────────────────────────────────────────────────┐
│  EXPLORI — Dashboard do Restaurante               [Logo] │
│  Olá, [Nome do Restaurante]          📅 Período: [Filtro]│
├─────────────┬───────────────────────────────────────────┤
│             │                                           │
│  MENU       │         ÁREA DE CONTEÚDO                  │
│             │                                           │
│  📊 Resumo  │                                           │
│  👥 Público │                                           │
│  🔄 Funil   │                                           │
│  🏆 Ranking │                                           │
│  🎟️ Promoções│                                          │
│  🔁 Retenção│                                           │
│             │                                           │
└─────────────┴───────────────────────────────────────────┘
```

### Tela 1 — Resumo Executivo
- 4 cards de KPI: Visualizações | Check-ins | Taxa de Conversão | Novos Clientes
- Gráfico de linha: evolução semanal/mensal de check-ins
- Alerta: "Seu restaurante está X% acima/abaixo da média da categoria"

### Tela 2 — Perfil do Público
- Gráfico de barras empilhadas: faixa etária × gênero
- Mapa de calor ou barras: top 10 cidades de origem dos visitantes
- Gráfico de hora do dia: quando os usuários buscam por restaurantes

### Tela 3 — Funil de Engajamento
- Funil visual: Visualizações → Saves → Check-ins → Recorrência
- Comparativo: seu funil vs média da categoria
- Destaque: "Você perde X% dos usuários entre visualização e check-in"

### Tela 4 — Ranking & Concorrência
- Tabela top 10 da sua categoria (check-ins e visualizações)
- Posição atual do restaurante destacada
- Gráfico de concorrência por faixa de gasto

### Tela 5 — Promoções e Vouchers
- Histograma: taxa de uso das promoções
- Comparativo: check-ins com voucher vs sem voucher
- Card: promoção mais eficaz vs menos eficaz

### Tela 6 — Retenção de Clientes
- Gráfico de barras: distribuição de check-ins por usuário
- Métrica: % de clientes que retornaram
- Recomendação automática: "Crie uma promoção para clientes que visitaram 1x para aumentar recorrência"

---

## 7. Paleta de Cores e Identidade Visual

Baseado na identidade visual já utilizada na análise exploratória:

| Elemento | Cor HEX | Uso |
|----------|---------|-----|
| Primária | `#E07A2F` | Barras, destaques, CTAs |
| Secundária | `#B96A4A` | Elementos complementares |
| Acento verde | `#6B7A3A` | Indicadores positivos / sucesso |
| Neutro | `#8A9450` | Gráficos de apoio |
| Fundo | `#F9F5F0` | Background do dashboard |
| Texto | `#2D2D2D` | Títulos e corpo |

---

## 8. Tecnologia Recomendada

| Componente | Tecnologia | Justificativa |
|-----------|-----------|--------------|
| Framework web | **Streamlit** | Já no stack do projeto (Aula 11), rápido para MVP |
| Gráficos | **Plotly Express** | Interatividade nativa, compatível com Streamlit |
| Dados | **Pandas** | Já utilizado na análise exploratória |
| Mapas | **Plotly Choropleth** ou **Folium** | Visualização geográfica de Pernambuco |
| Estilo | CSS customizado via `st.markdown` | Aplicar identidade Explori |

---

## 9. Filtros e Personalização

O dono do restaurante poderá filtrar os dados por:

- **Período**: últimos 7 dias / 30 dias / 90 dias / personalizado
- **Categoria do estabelecimento**: filtro por tipo de culinária/experiência
- **Faixa de gasto**: baixo / médio / alto
- **Região geográfica**: Recife / RMR / Interior

---

## 10. Insights Estratégicos Já Identificados (Base de Dados)

Estes insights, derivados da análise exploratória, devem aparecer no dashboard como **recomendações contextuais**:

1. **Horário de pico 13h–16h**: Ideal para publicar promoções ou ativar notificações push às 12h30.
2. **84% dos usuários fazem apenas 1 check-in**: Oportunidade crítica de retenção — cashback ou programa de fidelidade.
3. **Recife concentra ~46% dos usuários**: Para restaurantes fora do eixo central, segmentar campanhas para RMR pode ampliar alcance.
4. **Saves antecedem check-ins**: Usuários que salvam o perfil têm maior probabilidade de conversão — priorizar ações que incentivem o "save".
5. **Maioria das promoções não atinge 100% de uso**: Revisar mecânica, prazo de validade ou comunicação das promoções.
6. **Faixa de gasto "baixo" domina na maioria das categorias**: Restaurantes de ticket médio/alto devem investir em diferenciação de experiência para justificar o preço.
7. **Categorias de experiência têm distribuição mais equilibrada de gasto**: Oportunidade para restaurantes se posicionarem como "experiência gastronômica" além de simples refeição.

---

## 11. Fluxo de Dados (Arquitetura)

```
[dataset_eda_ficticio.zip]
         │
         ▼
  [ETL / Pandas]
  ├── usuarios.csv
  ├── estabelecimentos.csv
  ├── categorias.csv
  ├── checkins.csv
  ├── interacoes.csv
  └── promocoes.csv
         │
         ▼
  [Processamento]
  ├── Cálculo de KPIs
  ├── Agregações por estabelecimento
  ├── Filtros dinâmicos
  └── Geração de insights
         │
         ▼
  [Streamlit Dashboard]
  ├── Tela: Resumo
  ├── Tela: Público
  ├── Tela: Funil
  ├── Tela: Ranking
  ├── Tela: Promoções
  └── Tela: Retenção
```

---

## 12. Critérios de Aceitação (Padrão de Qualidade)

Baseados no documento "Padrão de aceitação dos graficos":

- [ ] Todos os gráficos possuem título claro e objetivo
- [ ] Eixos nomeados com unidade de medida
- [ ] Cores seguem a paleta Explori (`#E07A2F` como primária)
- [ ] Valores numéricos visíveis sobre barras/pontos
- [ ] Legenda quando houver mais de uma série
- [ ] Gráficos responsivos e sem sobreposição de rótulos
- [ ] Cada tela contém no mínimo 1 insight contextual em linguagem simples
- [ ] KPIs críticos têm comparativo com benchmark da plataforma
- [ ] Filtro de período funcional em todas as telas

---

*Documento gerado com base na análise exploratória `analise_dados_esplori_2025_2026.py` e nos documentos do projeto Explori.*
