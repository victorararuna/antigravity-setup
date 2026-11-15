---
name: peticionar-egm
description: Orquestra a skill consultar-leis com o padrão Elephant-Goldfish Model (EGM) usando 7 Goldfishes jurídicos especializados para busca profunda nos autos/acervo/web, redação exaustiva de petições ou pareceres e stress-test imparcial. Use quando precisar peticionar, revisar peça complexa ou fazer pesquisa jurídica profunda com múltiplos ângulos independentes.
---

# Peticionar EGM — 7 Goldfishes Jurídicos + `consultar-leis`

Este fluxo combina a memória e síntese do **Elefante** (agente coordenador) com **7 Goldfishes** em contexto isolado (`invoke_subagent`), garantindo busca profunda sem viés de confirmação e auditoria rigorosa antes do protocolo.

Sempre siga também as regras da skill `consultar-leis` (em especial `references/atuacao.md`, `references/peticao.md` e `references/citacao.md`).

---

## Os 7 Goldfishes

| Fase | Subagente (`TypeName`) | Papel |
| --- | --- | --- |
| **1. Busca Profunda** | `peticao-fatos-autos` | Auditoria fática e documental (exclusivamente ID + página do ID + transcrição literal) |
| **1. Busca Profunda** | `peticao-legislacao` | Pesquisa em `H:\acervo\leis` (`rodar.cmd`) e fontes oficiais, vigência e `versao_texto` |
| **1. Busca Profunda** | `peticao-jurisprudencia` | Pesquisa de precedentes reais no acervo e na web (metadados completos + ementa literal) |
| **1. Busca Profunda** | `peticao-processual` | Competência, cabimento, prazos, prescrição/decadência, tutela de urgência e pedidos |
| **3. Stress-Test** | `peticao-adversario` | Ataque pela ótica da parte contrária (preliminares, provas, sucumbência) |
| **3. Stress-Test** | `peticao-juiz` | Teste imparcial de decidibilidade (Delimitação → Normativa → Fática → Subsunção → Conclusão) |
| **3. Stress-Test** | `peticao-revisor` | Pente-fino final de transcrições literais, ID/página, metadados e fluidez técnica |

---

## Fluxo de Execução em 3 Fases

### Fase 1 — Busca Profunda em Paralelo (Goldfishes 1 a 4)

Quando o usuário pedir para peticionar, analisar autos ou fazer busca profunda:

1. Dispare **em paralelo** via `invoke_subagent`:
   - `peticao-fatos-autos` (passando os caminhos/conteúdos dos autos ou documentos fornecidos)
   - `peticao-legislacao` (passando o objeto jurídico, datas dos fatos e UF/município envolvidos)
   - `peticao-jurisprudencia` (passando as teses centrais e tribunais relevantes)
   - `peticao-processual` (passando o rito, tipo de peça pretendida e dados processuais disponíveis)
2. Aguarde os 4 relatórios sem preencher lacunas por conta própria.

### Fase 2 — Consolidação e Minuta (Elefante)

1. Consolide os achados dos Goldfishes 1 a 4. Se algum Goldfish apontou `"A informação não consta dos documentos disponibilizados."` em ponto essencial, sinalize ao usuário antes ou durante a minuta.
2. Redija a minuta completa (petição ou parecer) aplicando:
   - **Modo Parecerista/Advogado** (ou **Modo Judicial**, se solicitado);
   - Análise exaustiva, densa e fluida (sem rótulos escolares como *"premissa maior/menor"*);
   - **Transcrições literais** no bojo do texto;
   - Citação dos autos exclusivamente por **ID e página do ID**.
3. Salve a minuta em arquivo no workspace ou diretório de artefatos para que os Goldfishes revisores possam lê-la.

### Fase 3 — Stress-Test em Paralelo (Goldfishes 5 a 7)

1. Dispare **em paralelo** via `invoke_subagent`, passando o caminho da minuta e dos autos:
   - `peticao-adversario`
   - `peticao-juiz`
   - `peticao-revisor`
2. Aplique na minuta final todas as correções procedentes apontadas pelos 3 Goldfishes revisores e apresente ao usuário:
   - O caminho da minuta final revisada;
   - Os eventuais pontos críticos/lacunas probatórias que dependam de decisão ou documento do usuário.
