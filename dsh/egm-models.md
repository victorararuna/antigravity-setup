# EGM multi-modelo no DSH (perfil econômico)

O **Elefante** (agente principal) continua em `deepseek-account / deepseek-flash`.
Os **Goldfishes** são despachados com `subagent`, informando `provider` e `model` por chamada.

## Pré-requisitos

- Rota `openrouter` ativa: declarada em `~/.dsh/profiles/desktop/cordis.patch.yml`, chave `OPENROUTER_API_KEY` em `~/.dsh/.env`.
- Permissão ligada em **Plugins → Subagent**, com `openrouter` marcado. Sem isso o `provider`/`model` do subagente é ignorado.
- Autorizados hoje (chave `allowedModels` em `~/.dsh/profiles/desktop/cordis.patch.yml`): `deepseek-account/deepseek-flash` e os quatro free (`nemotron-3.5-super-vl`, `nemotron-3-ultra-550b-a55b`, `nano-omni-30b-a3b-reasoning`, `north-mini-code`). Um modelo fora dessa lista falha com "route is not allowed"; para usar outro, marque-o em Plugins → Subagente e salve (o harness reescreve o `allowedModels`).
- Se um modelo `:free` responder **404** (virou pago) ou **429** (rate limit), não insista: rode aquele papel no DeepSeek e avise.

## Mapa — pipeline EGM de design/código

Personas em `~/.dsh/skills/<skill>/agents/<arquivo>.md`.

| Persona (arquivo) | provider | model | Motivo |
|---|---|---|---|
| `zoom_out` | `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | contraponto de outra família no alto nível |
| `comprehension` | `openrouter` | `nvidia/nemotron-3.5-super-vl:free` | leitura e resumo, mecânico |
| `structural` | `openrouter` | `cohere/north-mini-code:free` | checagem de padrão estrutural |
| `style` | `openrouter` | `cohere/north-mini-code:free` | convenção de estilo/idioma |
| `inventive_catalyst` | `openrouter` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | divergência criativa |
| `codebase_details` | `deepseek-account` | `deepseek-flash` | precisão de símbolos e caminhos; não pode inventar |
| `design_critic` | `deepseek-account` | `deepseek-flash` | julgamento estético |
| `implementation_readiness` | `deepseek-account` | `deepseek-flash` | julgamento de viabilidade |
| `synthesizer` | `deepseek-account` | `deepseek-flash` | consolidação final |
| `bootstrap_orchestrator` | `deepseek-account` | `deepseek-flash` | coordenação |

## Mapa — jurídico (`peticionar-egm`)

Todos em `deepseek-account / deepseek-flash`, sem exceção:
`peticao-fatos-autos`, `peticao-legislacao`, `peticao-jurisprudencia`, `peticao-processual`, `peticao-adversario`, `peticao-juiz`, `peticao-revisor`.

Motivo: os sete trabalham com transcrição literal, ID e página do ID. Um modelo grátis trocando um dispositivo custa mais que qualquer crédito economizado. Para cortar custo no jurídico, corte volume de autos, não qualidade de conferência.

## Como despachar

```
subagent(
  description: "Goldfish zoom_out",
  prompt: "<conteúdo íntegro de agents/zoom_out.md>\n\n---\n\n<documento e parâmetros da tarefa>",
  provider: "openrouter",
  model: "nvidia/nemotron-3-ultra-550b-a55b:free"
)
```

- Leia o arquivo da persona e passe o texto **íntegro**; não parafraseie.
- Um Goldfish por chamada, sem histórico da conversa no prompt.
- Paralelize na mesma mensagem (várias chamadas de `subagent` juntas), respeitando o limite abaixo.

## Validação da saída

- O EGM exige relatório plano: uma linha por achado (severidade, `arquivo:linha`, problema, correção proposta).
- Saída vazia, prosa solta ou formato quebrado → reenvie uma vez com o formato explícito.
- Se falhar de novo, rode aquele papel no DeepSeek e registre no relatório que o Goldfish foi trocado.

## Limites operacionais

- **Paralelismo free:** no máximo 3 subagentes `:free` simultâneos. Acima disso o tier free devolve 429.
- **Isolamento:** no DSH o subagente herda todas as tools. A persona diz "read-only", mas é instrução de prompt, não sandbox — não peça a um Goldfish para escrever e depois confie que ele não escreveu.
- **Custo real:** free reduz dólares, não latência; o Nemotron Ultra é mais lento que o DeepSeek.
