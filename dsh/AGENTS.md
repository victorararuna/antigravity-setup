# Instruções globais — Victor (DSH)

## Regra jurídica inegociável

Nunca cite dispositivo legal, súmula, ato normativo ou precedente que não tenha sido lido diretamente no acervo
(`H:\acervo\leis`, ou o caminho em `DSH_LEIS_ACERVO`) ou em fonte oficial verificável.

- Se o texto não apareceu na consulta, diga que não foi localizado — nunca complete de memória.
- Antes de citar, confira o cabeçalho YAML da norma: `situacao` e `revogada` (norma revogada só como direito intertemporal) e `versao_texto` (texto compilado vs. publicação original).
- Se a norma não estiver no acervo, consulte a fonte oficial e informe que a conferência foi feita fora do acervo.
- Citação de autos: sempre por ID e página do ID, com transcrição literal.

## Skills disponíveis neste harness

| Skill | Quando usar |
|---|---|
| `consultar-leis` | Localizar norma, conferir vigência/redação, pesquisar jurisprudência real, parecer, petição, análise de autos |
| `peticionar-egm` | Petição ou pesquisa jurídica profunda: 7 Goldfishes em contexto isolado (4 de busca + 3 de stress-test) |
| `egm-bootstrap` | Documentar README.md por diretório de um repositório |
| `egm-brainstorm`, `egm-draft`, `egm-review`, `egm-resolve`, `egm-drift-report`, `egm-review-loop` | Pipeline EGM de design/revisão: brainstorm → draft → review → resolve → drift report |
| `unslop` | Refazer UI que parece gerada por IA (espaçamento, cor, ícones, copy, tipografia, layout, movimento) |

Regra de ouro do EGM: um Goldfish roda em contexto limpo, sem histórico da conversa. Nunca revise no mesmo contexto e chame de revisão Goldfish.

## Adaptação do EGM ao DSH

As skills `egm-*` e `peticionar-egm` foram escritas para vários harnesses. Aqui:

- A ferramenta de subagente é `subagent` (equivale a `invoke_subagent` no Antigravity, `Agent` no Claude Code, `spawn_agent` no Codex).
- Cada persona está em `agents/<nome>.md` **dentro da própria pasta da skill** (ex.: `~/.dsh/skills/egm-review/agents/zoom_out.md`), e os padrões em `resources/` da mesma skill.
- O DSH não registra subagentes nomeados por tipo: leia o arquivo da persona e passe o conteúdo íntegro no prompt do `subagent`. Não parafraseie a persona.
- Para rodar em paralelo, abra várias chamadas de `subagent` na mesma mensagem.
- **Mapa de modelos por persona (perfil econômico):** `~/.dsh/egm-models.md`. Siga-o ao despachar Goldfishes — grátis em `zoom_out`, `comprehension`, `structural`, `style` e `inventive_catalyst`; DeepSeek nas demais e em **todas** as personas jurídicas do `peticionar-egm`.

## Custo de modelos

Rota gratuita: `openrouter` (tier `:free`), declarada em `~/.dsh/profiles/desktop/cordis.patch.yml`, chave em `~/.dsh/.env` (`OPENROUTER_API_KEY`).
Modelos verificados funcionando: `nvidia/nemotron-3.5-super-vl:free` (rápido, multimodal), `nvidia/nemotron-3-ultra-550b-a55b:free`,
`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`, `cohere/north-mini-code:free`.

- Tarefa mecânica (rascunhar conteúdo, resumir, extrair, preencher dados de deck, boilerplate) → delegar via `subagent` com `provider: openrouter` e um modelo `:free`.
- Raciocínio, decisão de design/arquitetura, revisão final, análise jurídica → `deepseek-account/deepseek-flash`.
- Antes de confiar num `:free`, teste: `POST https://openrouter.ai/api/v1/chat/completions` com a chave do `.env`. Ids em catálogo podem já ter virado pagos (404) ou estar limitados (429).

## Onde está o acervo

- Skills e personas: `~/.dsh/skills/`
- Kit arquivado (não exposto ao catálogo): `~/.dsh/kit/` — canva, gdocs, gmail, gslides e as regras originais.
  Plugins Google e Canva dependem do CLI/login do Antigravity ou de um servidor MCP conectado; por isso ficam fora do catálogo.
  Para ativar um deles, copie a pasta para `~/.dsh/skills/<name>` usando o `name` do frontmatter (ex.: `canva-brand-check`).
- Espelho do repositório de origem: `~/antigravity-setup`. O `install.ps1` da raiz instala em `~/.gemini/config` (Antigravity); o `dsh/install.ps1` instala o kit no DSH.
- Documentação dos plugins (designs, harnesses, guias): `~/antigravity-setup/plugins/<plugin>/docs`.
- Atualizar o espelho: `git -C ~/antigravity-setup pull` (o clone já está com `http.sslBackend=openssl`; o git usa schannel e falha TLS sem isso).

As skills `egm-*` citam `docs/*.md` relativos ao plugin (`../../docs/...`) em trechos condicionais a outros harnesses (Codex, Claude Code); no DSH esses trechos não se aplicam — é a adaptação descrita acima. Para consultar esses docs, use o espelho.
