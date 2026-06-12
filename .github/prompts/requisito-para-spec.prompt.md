---
mode: ask
description: Transforma requisitos de negócio do dashboard Explori em um spec.md estruturado com user stories, critérios de aceitação e marcadores de incerteza. Use ao receber uma nova solicitação de funcionalidade antes de escrever qualquer código.
---

Transforme o seguinte requisito de negócio em um documento de especificação estruturado para o dashboard Explori.

**Nome da funcionalidade:** ${input:nomeFuncionalidade:Ex: Análise de Retenção de Clientes}
**Solicitado por / contexto:** ${input:contexto:Ex: dono de restaurante quer saber quais clientes voltaram mais de uma vez}
**Telas ou componentes afetados:** ${input:telasAfetadas:Ex: nova tela "Retenção", sidebar com novo filtro}
**Dados disponíveis no dataset:** ${input:dadosDisponiveis:Ex: checkins (id_usuario, data_hora_checkin, efetuou_checkin)}

---

## Protocolo de Transformação

Siga os 4 passos abaixo na ordem exata para gerar o `spec.md`.

---

### Passo 1 — Decomposição em User Stories

Para cada funcionalidade identificada no requisito, escreva uma user story no formato:

```
Como [persona],
quero [ação],
para que [benefício de negócio mensurável].
```

**Personas válidas neste projeto:**
- **Dono de restaurante** — usuário principal; baixo a médio letramento técnico; quer respostas rápidas e acionáveis
- **Gerente de operações** — analisa tendências; confortável com gráficos e tabelas
- **Atendente** — raramente usa; precisa de informação muito simples

**Regras para user stories:**
- Mínimo de **2 stories**, máximo de **5** por funcionalidade
- O benefício deve ser mensurável (ex: "reduzir churn em 10%", "identificar horário de pico")
- Evitar stories técnicas ("Como sistema, quero cachear os dados...") — foco no usuário

---

### Passo 2 — Critérios de Aceitação

Para cada user story, listar critérios de aceitação no formato **Given / When / Then**:

```
**AC-[número]:** [título curto]
- Given: [estado inicial / pré-condição]
- When: [ação do usuário]
- Then: [resultado esperado e verificável]
```

**Checklist obrigatório para todo critério que envolve gráfico:**
- [ ] Usa apenas cores da paleta Explori (`#E07A2F`, `#B96A4A`, `#6B7A3A`, `#8A9450`)
- [ ] Título do gráfico definido e descritivo
- [ ] Eixos nomeados em português
- [ ] Valores numéricos visíveis nas barras
- [ ] `insight-box` presente abaixo do gráfico
- [ ] Guarda `if not df.empty` implementada

**Checklist obrigatório para todo critério que envolve KPI:**
- [ ] Fórmula canônica utilizada (ver `copilot-instructions.md`)
- [ ] Comparação com benchmark da plataforma (conversão ≥35%, save ≥12%, compartilhamento ≥4%)
- [ ] `st.metric()` com `delta=` mostrando a meta

---

### Passo 3 — Mapeamento de Dados

Para cada story, mapear:

| Story | Tabela(s) necessária(s) | Colunas utilizadas | Transformação necessária |
|-------|------------------------|-------------------|------------------------|
| US-01 | | | |
| US-02 | | | |

**Verificar disponibilidade no dataset:**
- `usuarios`: `id_usuario`, `nome_usuario`, `genero`, `idade`, `origem_geografica`, `data_cadastro`
- `checkins`: `id_checkin`, `id_usuario`, `id_estabelecimento`, `data_hora_checkin`, `efetuou_checkin`
- `interacoes`: `id_usuario`, `id_estabelecimento`, `visualizacoes_perfil`, `saves_favoritos`, `compartilhamentos`, `data_hora_interacao`
- `promocoes`: `id_promocao`, `id_estabelecimento`, `tipo_promocao`, `quantidade_disponibilizada`, `quantidade_utilizada`, `data_inicio`, `data_fim`
- `categorias` + `estabelecimento_categoria`: para segmentação por tipo de restaurante

Se uma coluna necessária **não existe no dataset**, marcar como `[NEEDS CLARIFICATION]`.

---

### Passo 4 — Marcadores de Incerteza

Para cada item incerto, adicionar um dos três marcadores:

| Marcador | Quando usar | Exemplo |
|----------|------------|---------|
| `[NEEDS CLARIFICATION]` | Dado ou regra de negócio desconhecida, precisa de resposta do usuário | `[NEEDS CLARIFICATION] Qual é o período mínimo para considerar um cliente "retido"?` |
| `[ASSUMPTION]` | Decisão tomada sem confirmação explícita; pode mudar | `[ASSUMPTION] Considerando retenção como ≥2 check-ins no período` |
| `[OUT OF SCOPE]` | Mencionado mas não será implementado nesta versão | `[OUT OF SCOPE] Comparação entre restaurantes concorrentes` |

---

## Formato de Entrega — spec.md

Gere o documento completo no formato abaixo:

```markdown
# Spec: ${input:nomeFuncionalidade}

**Versão:** 1.0  
**Data:** [data atual]  
**Status:** Rascunho  
**Contexto:** ${input:contexto}

---

## User Stories

### US-01: [título]
> Como [persona], quero [ação], para que [benefício].

**Critérios de Aceitação:**

**AC-01:** [título]
- Given: ...
- When: ...
- Then: ...

[NEEDS CLARIFICATION / ASSUMPTION / OUT OF SCOPE se aplicável]

---

### US-02: [título]
...

---

## Mapeamento de Dados

| Story | Tabelas | Colunas | Transformação |
|-------|---------|---------|--------------|
| US-01 | | | |

---

## Incertezas e Riscos

| Marcador | Descrição | Responsável |
|----------|-----------|------------|
| [NEEDS CLARIFICATION] | ... | Dono do produto |
| [ASSUMPTION] | ... | Equipe dev |
| [OUT OF SCOPE] | ... | — |

---

## Checklist de Pré-Implementação

- [ ] Todas as `[NEEDS CLARIFICATION]` respondidas ou convertidas em `[ASSUMPTION]`
- [ ] Dataset validado — todas as colunas necessárias existem
- [ ] KPIs mapeados para fórmulas canônicas
- [ ] Nenhuma coluna de ID (`id_usuario`, `id_estabelecimento`) prevista na interface
- [ ] Gráficos planejados com paleta Explori confirmada
- [ ] Tela adicionada à navegação do sidebar
```

---

## Após gerar o spec.md

Confirme quais `[NEEDS CLARIFICATION]` precisam de resposta antes de prosseguir para implementação. Liste-as numeradas para facilitar a resposta do usuário.
