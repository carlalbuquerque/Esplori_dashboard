# Uso de IA no repositório — Explori Dashboard

Este documento descreve como a Inteligência Artificial (IA) é utilizada neste repositório, quais ferramentas/artefatos estão presentes, e as práticas recomendadas para colaboradores e avaliadores.

Objetivo
- Tornar explícito como Copilot, prompts e agentes são usados no fluxo de desenvolvimento.
- Fornecer regras de segurança, privacidade e revisão humana obrigatória.
- Ajudar o professor a avaliar a parte automatizada da entrega.

1) O que existe neste repositório relacionado à IA
- `.github/copilot-instructions.md`: instruções globais para GitHub Copilot e agentes (regras, paleta de cores, padrões de código).
- `.github/prompts/`: templates de prompts reutilizáveis para gerar specs, tarefas, telas e diagnósticos.
- `.github/agents/`: descrições de agentes (ex.: `dashboard-builder`, `data-analyst`, `security-reviewer`) que sintetizam workflows e papéis.
- `.github/skills/`: artefatos de conhecimento que agentes podem aplicar automaticamente (padrões de gráfico, schema, insights estratégicos).

2) Ferramentas e papéis
- GitHub Copilot: sugestão de código inline para acelerar implementações; respeitar as instruções em `copilot-instructions.md`.
- Agentes customizados (internos ao processo de desenvolvimento): definem tarefas repetíveis (criar tela, gerar spec, revisar código). Agentes não executam commits automaticamente sem revisão humana.
- Prompts: usados para gerar artefatos (specs, planos, templates de código) — cada prompt tem variáveis que devem ser preenchidas por um humano antes de execução completa.

3) Boas práticas e responsabilidades (obrigatórias)
- Revisão humana: TODO código gerado por IA deve ser revisado e testado por um desenvolvedor antes de merge.
- Privacidade: nunca enviar dados sensíveis (pessoais ou comerciais) para qualquer serviço de IA externo sem anonimização prévia.
- Atuação limitada: IA pode gerar sugestões e rascunhos — a aprovação final é humana.
- Attribution: quando um trecho significativo de código ou texto foi produzido por IA, adicione um comentário no commit/PR indicando que foi gerado com auxílio de Copilot/agent e descreva as modificações humanas realizadas.

4) Como usar os prompts e agents localmente (fluxo recomendado)
1. Abra o prompt na pasta `.github/prompts/` que corresponde à sua necessidade (ex.: `nova-tela-dashboard.prompt.md`).
2. Preencha as variáveis do prompt com contexto real do projeto (período, filtros, colunas esperadas).
3. Gere o texto usando Copilot/chat local (ou ambiente que suporte), revise e salve como `specs/<nome>.md`.
4. Se houver um agente (ex.: `dashboard-builder`), execute os passos manualmente: aplicar alterações, rodar `streamlit` e validar visualmente.

5) Exemplos de uso aceitáveis
- Gerar um esboço de função `carregar_dados()` a partir do schema em `.github/skills/dataset-schema.md` e depois ajustar tipos e validações manualmente.
- Criar um draft de `plot_funil()` usando os padrões em `plotly-patterns.md` e depois revisar texto e cores.

6) O que NÃO deve ser feito
- Não aceitar patches/PRs automatizados de agentes sem revisão de um desenvolvedor.
- Não enviar CSVs com dados pessoais identificáveis para serviços de geração de código.
- Não usar IA para gerar credenciais, chaves ou secrets — essas ações são proibidas.

7) Auditoria e rastreabilidade
- Documente no PR/commit as mensagens: "Gerado com auxílio de Copilot — revisado por <nome>".
- Para trabalhos avaliativos, inclua no relatório as versões dos prompts usados (copiar o conteúdo do prompt ou referenciar o arquivo em `.github/prompts/`).

8) Suporte e dúvidas
- Se tiver dúvidas sobre um trecho gerado por IA, abra uma issue com a tag `ia-review` e descreva o trecho e a preocupação.

9) Declaração final para avaliação
- Este repositório usa IA como assistente (sugestões, templates e automação parcial). Todas as entregas de código foram/serão validadas por desenvolvedores humanos antes do envio final.

---
