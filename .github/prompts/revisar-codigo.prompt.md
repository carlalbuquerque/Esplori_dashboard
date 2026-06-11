---
mode: ask
description: Revisa um trecho de código Python do projeto Explori verificando segurança, padrões de dados e qualidade dos gráficos. Use antes de fazer commit de qualquer alteração no dashboard.
---

Faça uma revisão completa do seguinte trecho de código do projeto Explori Dashboard:

**Arquivo:** ${input:arquivo:Ex: dashboard_donos.py}
**Funcionalidade:** ${input:funcionalidade:Ex: tela de retenção de clientes, função carregar_dados, gráfico de funil}

Cole o código a ser revisado abaixo ou referencie o arquivo aberto.

---

## Critérios de Revisão

Execute os três blocos de verificação abaixo e reporte **todos** os achados, incluindo os itens aprovados.

---

### BLOCO 1 — Segurança e Privacidade de Dados (LGPD)

- [ ] Colunas `id_usuario`, `id_estabelecimento`, `id_checkin`, `id_promocao` **não aparecem** em `st.dataframe()`, `st.table()`, `st.write()` ou em qualquer saída visível ao usuário
- [ ] Dados de `idade`, `genero` e `origem_geografica` exibidos apenas de forma **agregada** (nunca linha a linha)
- [ ] Nenhum `print()` de debug expõe dados pessoais em produção
- [ ] `st.session_state` não armazena DataFrames completos com dados individuais de usuários
- [ ] Caminho do ZIP construído com `os.path.join()` e com verificação de path traversal

**Severidade dos achados:** 🔴 Crítico (expõe dado pessoal) | 🟡 Médio (risco potencial) | 🟢 Baixo (melhoria)

---

### BLOCO 2 — Padrões de Dados e Pipeline

- [ ] `@st.cache_data` presente em todas as funções de carregamento
- [ ] Dados tratados na ordem: padronizar → preencher nulos → remover duplicatas → calcular KPIs
- [ ] Verificação `if not df.empty` antes de **todo** gráfico
- [ ] Nulos tratados conforme o schema canônico:
  - `genero` → `.fillna("não informado")`
  - `origem_geografica` → `.fillna(moda)` + `.str.lower().str.strip()`
  - `efetuou_checkin` → `.fillna(False).astype(bool)`
  - `visualizacoes_perfil`, `saves_favoritos`, `compartilhamentos` → `.fillna(0).astype(int)`
  - `quantidade_disponibilizada` → `.fillna(mediana)`
  - `idade` → `dropna()` + filtro `18 <= idade <= 65`
- [ ] KPIs calculados com as fórmulas canônicas do projeto

---

### BLOCO 3 — Qualidade dos Gráficos Plotly

Para cada gráfico encontrado no código:

- [ ] `title=` definido e descritivo
- [ ] `labels={}` com nomes dos eixos em português
- [ ] `text=coluna` com `textposition="outside"` (barras)
- [ ] `color_discrete_sequence` ou `color_discrete_map` mapeado para paleta Explori
  - Primária: `#E07A2F` | Verde: `#6B7A3A` | Secundária: `#B96A4A` | Neutro: `#8A9450`
- [ ] `plot_bgcolor="white"` e `paper_bgcolor="white"` no `update_layout`
- [ ] `st.plotly_chart(fig, use_container_width=True)`
- [ ] `insight-box` imediatamente após o gráfico
- [ ] **Nenhuma** cor padrão do Plotly em uso

---

## Formato do Relatório de Revisão

Para cada item com falha:

```
[BLOCO X] 🔴/🟡/🟢 — [Descrição do problema]
📍 Linha(s): X–Y
🔍 Problema: [Explicação]
✅ Correção:
[código corrigido]
```

Ao final, emita um resumo:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESUMO DA REVISÃO — ${input:arquivo}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Críticos:  X
🟡 Médios:    X
🟢 Baixos:    X
✅ Aprovados: X / [total de itens verificados]

Veredicto: ✅ APROVADO | ⚠️ APROVADO COM RESSALVAS | 🔴 REPROVADO
```
