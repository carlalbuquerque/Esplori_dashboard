---
description: Padrões e templates Plotly/Streamlit específicos do projeto Explori Dashboard. Ativada em arquivos Python para garantir que todos os gráficos sigam a identidade visual e os critérios de qualidade do projeto.
applyTo: "**/*.py"
---

# Padrões Plotly — Explori Dashboard

Esta skill contém os templates canônicos de gráficos para o projeto. Sempre que gerar ou modificar um gráfico em qualquer arquivo `.py`, use os padrões abaixo.

---

## Regras Absolutas

1. **Nunca** usar `color_discrete_sequence` padrão do Plotly — sempre mapear para a paleta Explori
2. **Nunca** omitir `plot_bgcolor="white", paper_bgcolor="white"`
3. **Nunca** chamar `st.plotly_chart(fig)` sem `use_container_width=True`
4. **Sempre** incluir `insight-box` logo abaixo de cada gráfico
5. **Sempre** verificar `if not df.empty` antes de criar o gráfico

---

## Paleta (memorizar)

```python
COR_PRIMARIA   = "#E07A2F"   # principal
COR_SECUNDARIA = "#B96A4A"   # complementar
COR_VERDE      = "#6B7A3A"   # positivo / sucesso
COR_NEUTRO     = "#8A9450"   # terceira série
COR_FUNDO      = "#F9F5F0"   # fundo
COR_TEXTO      = "#2D2D2D"   # texto
```

---

## Template: Gráfico de Barras Verticais

```python
if not df.empty:
    fig = px.bar(
        df,
        x="coluna_x",
        y="coluna_y",
        color_discrete_sequence=[COR_PRIMARIA],
        text="coluna_y",
        labels={"coluna_x": "Rótulo do Eixo X", "coluna_y": "Rótulo do Eixo Y"},
        title="Título Claro e Objetivo",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=COR_TEXTO),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-box">💡 <strong>Insight:</strong> Texto aqui.</div>',
        unsafe_allow_html=True,
    )
```

---

## Template: Gráfico de Barras Horizontais (ranking)

```python
if not df.empty:
    df_sorted = df.sort_values("coluna_valor")  # ascendente para barras horizontais
    fig = px.bar(
        df_sorted,
        x="coluna_valor",
        y="coluna_categoria",
        orientation="h",
        color_discrete_sequence=[COR_PRIMARIA],
        text="coluna_valor",
        labels={"coluna_valor": "Valor", "coluna_categoria": "Categoria"},
        title="Top N — [Descrição]",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=COR_TEXTO),
        yaxis=dict(autorange="reversed"),  # maior valor no topo
    )
    st.plotly_chart(fig, use_container_width=True)
```

---

## Template: Gráfico de Barras Agrupadas (comparativo)

```python
if not df.empty:
    fig = px.bar(
        df,
        x="coluna_x",
        y="coluna_y",
        color="coluna_grupo",
        barmode="group",
        color_discrete_sequence=[COR_PRIMARIA, COR_VERDE, COR_SECUNDARIA],
        labels={"coluna_grupo": "Legenda"},
        title="Comparativo — [Descrição]",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=COR_TEXTO),
    )
    st.plotly_chart(fig, use_container_width=True)
```

---

## Template: Gráfico de Barras Empilhadas (composição)

```python
if not df.empty:
    fig = px.bar(
        df,
        x="coluna_x",
        y="coluna_y",
        color="coluna_grupo",
        barmode="stack",
        color_discrete_sequence=[COR_PRIMARIA, COR_SECUNDARIA, COR_NEUTRO, COR_VERDE],
        title="Composição — [Descrição]",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=COR_TEXTO),
        xaxis=dict(tickangle=45),
    )
    st.plotly_chart(fig, use_container_width=True)
```

---

## Template: Gráfico de Pizza / Donut

```python
if not df.empty:
    fig = px.pie(
        df,
        names="coluna_categoria",
        values="coluna_valor",
        color_discrete_sequence=[COR_PRIMARIA, COR_VERDE, COR_SECUNDARIA, COR_NEUTRO],
        hole=0.45,  # 0 para pizza sólida, 0.45 para donut
        title="Distribuição — [Descrição]",
    )
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(color=COR_TEXTO),
    )
    st.plotly_chart(fig, use_container_width=True)
```

---

## Template: Funil de Engajamento

```python
import plotly.graph_objects as go

if etapas and valores:
    fig = go.Figure(go.Funnel(
        y=["Visualizações", "Saves", "Compartilhamentos", "Check-ins"],
        x=[total_views, total_saves, total_shares, total_checkins],
        textinfo="value+percent initial",
        marker=dict(color=[COR_PRIMARIA, COR_SECUNDARIA, COR_NEUTRO, COR_VERDE]),
    ))
    fig.update_layout(
        title="Funil de Engajamento",
        paper_bgcolor="white",
        font=dict(color=COR_TEXTO),
    )
    st.plotly_chart(fig, use_container_width=True)
```

---

## Template: Histograma

```python
if not df.empty:
    fig = px.histogram(
        df,
        x="coluna_numerica",
        nbins=10,
        color_discrete_sequence=[COR_PRIMARIA],
        labels={"coluna_numerica": "Descrição do eixo X"},
        title="Distribuição — [Descrição]",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis_title="Quantidade",
        font=dict(color=COR_TEXTO),
    )
    st.plotly_chart(fig, use_container_width=True)
```

---

## Template: Gráfico de Linha (série temporal)

```python
if not df.empty:
    fig = px.line(
        df,
        x="coluna_data",
        y="coluna_valor",
        color_discrete_sequence=[COR_PRIMARIA],
        markers=True,
        labels={"coluna_data": "Data", "coluna_valor": "Valor"},
        title="Evolução — [Descrição]",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=COR_TEXTO),
    )
    st.plotly_chart(fig, use_container_width=True)
```

---

## Template: Cards de KPI (`st.metric`)

```python
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    label="👁️ Visualizações",
    value=f"{total_views:,}",
)
c2.metric(
    label="📍 Check-ins",
    value=f"{total_checkins:,}",
)
c3.metric(
    label="🎯 Taxa de Conversão",
    value=f"{taxa_conversao:.1%}",
    delta="Meta: ≥35%",
    delta_color="normal",
)
c4.metric(
    label="❤️ Taxa de Save",
    value=f"{taxa_save:.1%}",
    delta="Meta: ≥12%",
    delta_color="normal",
)
```

---

## CSS Obrigatório (inserir no início do arquivo, após `st.set_page_config`)

```python
COR_PRIMARIA = "#E07A2F"
COR_FUNDO    = "#F9F5F0"

st.markdown(
    f"""
    <style>
        .block-container {{ background-color: {COR_FUNDO}; padding-top: 1.5rem; }}
        h1, h2, h3 {{ color: #2D2D2D; }}
        .insight-box {{
            background: #FFF8F0;
            border-left: 4px solid {COR_PRIMARIA};
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-size: 0.9rem;
            color: #4A3728;
            margin-top: 0.5rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)
```

---

## Checklist Final Antes de Entregar Qualquer Gráfico

- [ ] `if not df.empty` presente antes do bloco de plot
- [ ] `title=` definido e descritivo
- [ ] `labels={}` com nomes de eixos em português e legíveis
- [ ] `color_discrete_sequence` ou `color_discrete_map` mapeado para paleta Explori
- [ ] `plot_bgcolor="white"` e `paper_bgcolor="white"` no `update_layout`
- [ ] `st.plotly_chart(fig, use_container_width=True)`
- [ ] `insight-box` imediatamente após o gráfico
