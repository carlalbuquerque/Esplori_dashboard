# Explori Dashboard — Dashboard para Estabelecimentos

Painel Streamlit que transforma dados de check-ins, visualizações, saves e promoções em insights acionáveis para donos e gerentes de restaurantes na plataforma Explori.

## Visão geral
- Aplicação: painel interativo com páginas para Perfil do Público, Engajamento, Retenção, Promoções e Benchmarking.
- Tech: Python 3.10+, Streamlit, Pandas, Plotly.
- Dados: CSVs sob `data/extracted/` (fornecidos no repositório).

## Requisitos
- Python 3.10+
- Recomendado criar virtualenv no diretório do projeto

## Instalação (Windows / PowerShell)
1. Criar e ativar virtualenv:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
2. Atualizar pip e instalar dependências:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Rodando o dashboard
Em ambiente virtual ativado, a partir da raiz do projeto:
```powershell
streamlit run app.py
```
A aplicação abre em `http://localhost:8501` por padrão.

Se o navegador mostrar uma versão antiga (ou uma página removida como "Visão Geral"):
- Faça hard refresh (Ctrl+F5) ou abra em janela anônima.
- No menu do Streamlit: "Rerun" → "Clear cache and rerun".
- Alternativamente reinicie o servidor Streamlit.

## Estrutura principal do repositório
- `app.py` — bootstrap, rotas e sidebar.
- `views/` — páginas do dashboard (ex.: `perfil_publico.py`, `promocoes.py`, `benchmarking.py`, `engajamento.py`, `retencao.py`).
- `utils/` — utilitários (ex.: `dados.py`, `constantes.py`, `assets/`).
- `data/extracted/` — CSVs de entrada.
- `documento projeto/` — análises e documentos de apoio.

## Convenções importantes (resumo)
- Idioma: variáveis e funções em português (ex.: `usuarios`, `checkins`, `carregar_dados()`).
- Cache: funções de carga/transf. pesadas devem usar `@st.cache_data`.
- Verificação: sempre `if not df.empty` antes de plotar.
- Formatação de datas: `pd.to_datetime(..., errors='coerce')`.
- Tratamento de nulos: siga as regras em `.github/instructions`.

## Paleta de cores do projeto (obrigatória)
Definida em `utils/constantes.py` — usar sempre essas constantes em gráficos:
- `COR_PRIMARIA = "#E07A2F"`
- `COR_SECUNDARIA = "#B96A4A"`
- `COR_VERDE = "#6B7A3A"`
- `COR_NEUTRO = "#8A9450"`
- `COR_FUNDO = "#F9F5F0"`
- `COR_TEXTO = "#2D2D2D"`

Nos gráficos Plotly, sempre mapear cores via `color_discrete_sequence`/`color_discrete_map` e setar:
```py
fig.update_layout(plot_bgcolor=COR_FUNDO, paper_bgcolor=COR_FUNDO, font=dict(color=COR_TEXTO))
```

## Padrões de gráfico (checklist rápido)
- Título claro.
- Eixos nomeados (com unidades quando aplicável).
- Valores numéricos visíveis (`text=` + `textposition="outside"` para barras).
- Legenda presente para múltiplas séries.
- `st.plotly_chart(fig, use_container_width=True)` para responsividade.
- Caixa de insight logo abaixo do gráfico (HTML/CSS padrão do projeto).

## Dados
Colocar o zip/CSVs em `data/` conforme estrutura:
- `usuarios.csv`, `estabelecimentos.csv`, `categorias.csv`, `estabelecimento_categoria.csv`, `checkins.csv`, `interacoes.csv`, `promocoes.csv`

A função de carregamento em `utils/dados.py` realiza limpeza inicial (normaliza cabeçalhos, trata nulos e converte datas).

## Desenvolvimento
- Faça alterações em `views/` para novas páginas ou ajustes visuais.
- Use `utils/constantes.py` para cores e `CSS_CUSTOMIZADO` para estilos globais.
- Ao remover/renomear páginas, atualize `app.py` (rotas e `_OPCOES`) e reinicie Streamlit.
- Para depuração de `st.session_state`, use o painel do Streamlit e recarregue a página.

## Troubleshooting rápido
- Erro de import após remoção de arquivo de view: remova referências em `app.py`/`dashboard_donos.py`.
- KeyError em colunas: verifique cabeçalhos CSV (aspas/remanescentes) e execute `carregar_dados()` com inspeção.
- Sessão exibindo página removida: reiniciar servidor + hard refresh do navegador.

## Testes e verificações
- Não há suíte de testes automatizada incluída; para validação manual:
	- Verificar carregamento sem exceção ao executar `streamlit run app.py`.
	- Testar cada página via sidebar e inspecionar gráficos quanto à paleta/legibilidade.

## Contribuição
- Siga os padrões de nomenclatura e paleta.
- Abra PR com descrição curta das mudanças de UX/visual.
- Sempre valide que `@st.cache_data` está presente em funções de leitura/agregação pesadas.

## Licença
- Adicione aqui a licença do seu projeto (ex.: MIT) se aplicável.
