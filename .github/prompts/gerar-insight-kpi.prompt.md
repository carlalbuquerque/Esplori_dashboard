---
mode: ask
description: Gera um insight estratégico completo com análise baseada nos dados reais do dataset Explori. Use este prompt para criar recomendações acionáveis para donos de restaurantes.
---

Gere um insight estratégico completo para um dono de restaurante com base nos dados da plataforma Explori.

**KPI analisado:** ${input:kpi:Ex: taxa de conversão, retenção, uso de promoções, faixa etária}
**Valor atual medido:** ${input:valorAtual:Ex: 28% de taxa de conversão}
**Contexto do restaurante:** ${input:contexto:Ex: restaurante japonês, faixa de gasto médio, localizado em Recife}

---

## Instruções para geração do insight

### 1. Calcular com fórmulas canônicas
Use exclusivamente as fórmulas abaixo para o KPI **${input:kpi}**:

```python
taxa_conversao    = len(checkins) / interacoes["visualizacoes_perfil"].sum()
taxa_save         = interacoes["saves_favoritos"].sum() / interacoes["visualizacoes_perfil"].sum()
taxa_compartilhar = interacoes["compartilhamentos"].sum() / interacoes["visualizacoes_perfil"].sum()
taxa_uso_promo    = promocoes["quantidade_utilizada"] / promocoes["quantidade_disponibilizada"]
taxa_retencao     = (retencao["num_checkins"] >= 2).sum() / len(retencao)
```

### 2. Comparar com benchmarks da plataforma

| KPI | Meta Explori |
|-----|-------------|
| Taxa de conversão | ≥ 35% |
| Taxa de save | ≥ 12% |
| Taxa de compartilhamento | ≥ 4% |

O valor atual **${input:valorAtual}** está: acima / dentro / abaixo da meta? Declare explicitamente.

### 3. Cruzar com os insights estratégicos confirmados
Relacione o resultado com pelo menos um destes fatos do dataset real:
- Pico de buscas: 13h–16h (melhor horário para publicar promoções: 12h30)
- 84% dos usuários fazem apenas 1 check-in — oportunidade crítica de retenção
- Recife concentra ~46% dos usuários — centralização metropolitana
- Saves antecedem check-ins: usuários que salvam têm +29% de chance de converter
- Maioria das promoções não atinge 100% de uso — revisar mecânica e comunicação
- Faixa "baixo" domina: restaurantes de ticket alto devem apostar em experiência
- Funil clássico: visualizações >> saves >> compartilhamentos >> check-ins

### 4. Estrutura obrigatória de entrega

```
📊 ANÁLISE: [Nome do KPI]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Resultado: ${input:valorAtual} vs Meta: [benchmark]
Status: ✅ Acima | ⚠️ Na margem | 🔴 Abaixo

🔍 O que significa:
[Explicação em 2–3 frases, sem jargão técnico, para o dono do restaurante]

💡 Recomendação imediata (próximas 48h):
[Ação específica e mensurável]

🗓️ Recomendação de médio prazo (próximas 4 semanas):
[Estratégia baseada nos padrões do dataset]

⚠️ Atenção:
[Limitação ou dado que precisa de monitoramento]
```

### 5. Gerar o código da insight-box para o dashboard

Gere também o bloco Python pronto para ser inserido no `dashboard_donos.py`:

```python
st.markdown(
    '<div class="insight-box">💡 <strong>Insight:</strong> [Texto gerado]</div>',
    unsafe_allow_html=True,
)
```

O texto deve ser conciso (máximo 2 frases), direto e acionável.
