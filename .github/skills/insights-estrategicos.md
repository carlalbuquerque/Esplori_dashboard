---
description: Insights estratégicos confirmados pela análise exploratória do dataset Explori 2025-2026. Ativa automaticamente para garantir que recomendações geradas no dashboard sejam baseadas em evidências reais dos dados.
alwaysApply: true
---

# Insights Estratégicos — Explori Dashboard

Estes insights foram **confirmados pela análise exploratória** do dataset real da plataforma Explori (2025-2026). Sempre que o Copilot gerar textos de insight, recomendações ou caixas `insight-box` no dashboard, deve referenciar estes fatos — nunca inventar números ou padrões.

---

## Insight 1 — Horário de Pico de Busca

**Fato confirmado:** Concentração de buscas entre **13h e 16h**, com pico às **14h**.

**Implicação para o dashboard:**
- Caixas de insight na tela "Perfil do Público" devem mencionar este horário
- Recomendação padrão: *"Publique promoções e atualize seu perfil às 12h30 para capturar o público no momento de maior intenção de descoberta."*

**Evidência no código de análise:**
```python
usuarios["hora"].value_counts().sort_index()
# Resultado: pico às 14h, alta entre 13h–16h
```

---

## Insight 2 — Retenção: 84% fazem 1 único check-in

**Fato confirmado:** Aproximadamente **84% dos usuários realizam apenas 1 check-in**. Usuários com 3+ check-ins representam ~1,66% da base.

**Implicação para o dashboard:**
- Tela "Retenção de Clientes" deve sempre destacar este número como **maior oportunidade de crescimento**
- Recomendação padrão: *"Crie uma oferta exclusiva para a segunda visita — transformar visitantes únicos em recorrentes é o maior alavancador de receita disponível."*

**Evidência:**
```python
retencao = checkins.groupby("id_usuario").size()
# 84% dos usuários têm size == 1
```

---

## Insight 3 — Concentração Geográfica em Recife

**Fato confirmado:** **Recife concentra ~46% dos usuários** (2.625 de ~5.673). As demais cidades da RMR (Olinda, Jaboatão, Paulista) somam mais ~30%. Cidades do interior têm participação marginal.

**Implicação para o dashboard:**
- Gráfico de origem geográfica deve ter nota sobre viés metropolitano
- Recomendação para restaurantes fora da RMR: *"Segmente campanhas para o público da Região Metropolitana — esse é o perfil que mais descobre novos estabelecimentos na plataforma."*

**Evidência:**
```python
usuarios["origem_geografica"].value_counts()
# Recife: 2625 (topo destacado)
```

---

## Insight 4 — Saves Antecedem Check-ins

**Fato confirmado:** Usuários que fizeram check-in apresentam médias maiores de:
- `visualizacoes_perfil`: 6,21 (com check-in) vs 5,72 (sem check-in) → **+8,5%**
- `saves_favoritos`: 0,88 (com check-in) vs 0,68 (sem check-in) → **+29,4%**

Correlação `visualizacoes_perfil` → `saves_favoritos`: **r ≈ 0,28** (moderada positiva).

**Implicação para o dashboard:**
- Funil deve destacar o "save" como etapa crítica de intenção
- Recomendação padrão: *"Incentive o 'Salvar' com chamadas visuais no seu perfil — usuários que salvam têm 29% mais chance de fazer check-in."*

**Evidência:**
```python
df_merge.groupby("fez_checkin")[["visualizacoes_perfil", "saves_favoritos"]].mean()
```

---

## Insight 5 — Maioria das Promoções Não Atinge 100% de Uso

**Fato confirmado:** A distribuição da `taxa_uso` das promoções mostra que a **maioria das promoções não é totalmente aproveitada** — poucas atingem `taxa_uso = 1.0`.

**Implicação para o dashboard:**
- Histograma de taxa de uso deve incluir linha de referência em 70% (benchmark mínimo de boa performance)
- Recomendação padrão: *"Revise o prazo de validade, o valor do desconto e o canal de divulgação das promoções com baixo aproveitamento (<30%)."*

---

## Insight 6 — Faixa de Gasto "Baixo" Domina Todas as Categorias

**Fato confirmado:** Na análise de concorrência por categoria e faixa de gasto, a faixa `"baixo"` é **dominante em praticamente todas as categorias**. A faixa `"alto"` representa o menor segmento.

**Implicação para o dashboard:**
- Gráfico de concorrência deve usar legenda diferenciando as faixas com as cores do projeto
- Recomendação para restaurantes de ticket alto: *"Diferencie-se pela experiência gastronômica — o público que investe mais espera valor percebido além do prato."*

---

## Insight 7 — Funil Clássico com Queda Acentuada em Compartilhamentos

**Fato confirmado:** O funil de engajamento segue padrão clássico com queda progressiva:

```
Visualizações (20.002) >> Saves (~ 8k) >> Compartilhamentos (muito baixo) >> Check-ins
```

Correlações confirmadas:
- `visualizacoes_perfil` → `compartilhamentos`: **r ≈ 0,18** (fraca)
- `saves_favoritos` → `compartilhamentos`: **r ≈ 0,07** (muito fraca)

**Implicação para o dashboard:**
- O funil visual deve mostrar claramente o drop-off em cada etapa
- Compartilhamento **não deve ser tratado como proxy de conversão** — é comportamento social distinto
- Recomendação padrão: *"Foque em aumentar saves (intenção) antes de compartilhamentos (alcance social) — a conversão segue o save, não o share."*

---

## Benchmarks da Plataforma (Referência para Cards de KPI)

| KPI | Meta mínima | Interpretação se abaixo da meta |
|-----|------------|---------------------------------|
| Taxa de conversão view→check-in | **≥ 35%** | Perfil desatualizado, sem promoções ativas ou categoria com baixa demanda |
| Taxa de save | **≥ 12%** | Fotos de baixa qualidade ou ausência de informações atrativas no perfil |
| Taxa de compartilhamento | **≥ 4%** | Experiência não memorável ou sem gatilhos de recomendação |

Estes benchmarks devem aparecer como `delta` nos `st.metric()` do Resumo Executivo.
