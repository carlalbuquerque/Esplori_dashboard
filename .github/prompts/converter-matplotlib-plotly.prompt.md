---
mode: ask
description: Converte um gráfico Matplotlib existente (do script de análise exploratória) para Plotly seguindo os padrões visuais do dashboard Explori. Use ao migrar análises do Colab para o dashboard.
---

Converta o seguinte gráfico Matplotlib para Plotly, aplicando os padrões visuais do dashboard Explori.

**Nome do gráfico:** ${input:nomeGrafico:Ex: Distribuição por Faixa Etária e Gênero}
**Tipo de gráfico Plotly desejado:** ${input:tipoPlotly:Ex: px.bar, px.pie, px.histogram, go.Funnel}
**Título para o dashboard:** ${input:titulo:Ex: Perfil do Público — Faixa Etária × Gênero}
**Insight estratégico relacionado:** ${input:insight:Ex: Faixas 26-35 e 56-65 têm maior presença; gênero masculino levemente predominante}

Cole o código Matplotlib original abaixo para conversão:

---

## Regras de Conversão

### Paleta Obrigatória (nunca usar cores padrão do Plotly)

```python
COR_PRIMARIA   = "#E07A2F"   # série principal / destaque
COR_SECUNDARIA = "#B96A4A"   # segunda série
COR_VERDE      = "#6B7A3A"   # indicadores positivos
COR_NEUTRO     = "#8A9450"   # terceira série
```

### Mapeamento Matplotlib → Plotly

| Matplotlib | Plotly equivalente |
|-----------|-------------------|
| `plt.bar()` / `ax.bar()` | `px.bar(..., orientation="v")` |
| `plt.barh()` / `ax.barh()` | `px.bar(..., orientation="h")` |
| `plt.plot()` | `px.line()` |
| `plt.hist()` | `px.histogram()` |
| `plt.pie()` | `px.pie(hole=0.45)` |
| `demo.plot(kind="bar", stacked=True)` | `px.bar(..., barmode="stack")` |
| Funil manual | `go.Figure(go.Funnel(...))` |
| `plt.text()` sobre barras | `text="coluna"` + `textposition="outside"` |
| `plt.title()` | `title=` no `px.*` |
| `plt.xlabel()` / `plt.ylabel()` | `labels={"x": "...", "y": "..."}` |
| `plt.legend()` | automático com `color=` |
| `plt.grid(axis="y")` | removido — usar fundo branco |
| `plt.tight_layout()` | removido — Plotly é responsivo |

### Itens obrigatórios no código convertido

```python
if not df.empty:
    fig = px.${input:tipoPlotly}(
        df,
        # ... parâmetros
        color_discrete_sequence=[COR_PRIMARIA, COR_SECUNDARIA, COR_VERDE, COR_NEUTRO],
        text="coluna_valor",          # para barras
        title="${input:titulo}",
        labels={"col": "Rótulo"},
    )
    fig.update_traces(textposition="outside")   # para barras
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#2D2D2D"),
        xaxis=dict(tickangle=45),               # se labels longos
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-box">💡 <strong>Insight:</strong> ${input:insight}</div>',
        unsafe_allow_html=True,
    )
```

---

## Formato de entrega

1. **Código Plotly completo** — pronto para ser colado no `dashboard_donos.py`
2. **Diff resumido** — lista das mudanças feitas (ex: "substituído `plt.bar` por `px.bar`, adicionado `insight-box`, mapeadas cores para paleta Explori")
3. **Checklist de qualidade** — confirmar que todos os itens abaixo estão presentes:
   - [ ] `title=` definido
   - [ ] `labels={}` com eixos nomeados
   - [ ] `text=` com `textposition="outside"` (se barras)
   - [ ] `color_discrete_sequence` mapeado para paleta Explori
   - [ ] `plot_bgcolor="white"` e `paper_bgcolor="white"`
   - [ ] `st.plotly_chart(fig, use_container_width=True)`
   - [ ] `insight-box` presente com o insight: **${input:insight}**
