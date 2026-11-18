# Kit DSH (DeepSeek Harness)

Configuração do harness que complementa o pacote de Antigravity deste repositório.

## O que este diretório instala

| Item | Destino |
|---|---|
| `skills/consultar-leis`, `skills/unslop` | `~/.dsh/skills/` |
| `plugins/egm/skills/*` + `agents/` + `resources/` embutidos | `~/.dsh/skills/egm-*/` |
| `plugins/peticionar-egm` (skill + 7 Goldfishes) | `~/.dsh/skills/peticionar-egm/` |
| `dsh/AGENTS.md` | `~/.dsh/AGENTS.md` |
| `dsh/egm-models.md` (mapa de modelos por persona) | `~/.dsh/egm-models.md` |
| `dsh/profile/cordis.patch.yml` (rota free + política de subagente) | `~/.dsh/profiles/desktop/cordis.patch.yml` |
| `plugins/canva`, `gdocs`, `gmail`, `gslides`, `rules/` | `~/.dsh/kit/` (arquivados, fora do catálogo) |

## Instalação

```powershell
git clone https://github.com/victorararuna/antigravity-setup "$HOME\antigravity-setup"
& "$HOME\antigravity-setup\dsh\install.ps1"
```

Depois:

1. Coloque a chave do OpenRouter em `~/.dsh/.env` (`OPENROUTER_API_KEY=...`) — o script cria o arquivo vazio.
2. **Reinicie o DeepSeek Harness** (o patch de perfil é lido no boot).
3. Em **Plugins → Subagente**, ligue "Permitir que os agentes escolham modelos para subagentes", marque as rotas e **Salve**.
4. A política vale **apenas para sessões novas**.

## Por que as skills não são copiadas como estão

O DSH descobre skills em `<raiz>/<nome>/SKILL.md` e não tem registro de subagentes por tipo. Duas adaptações:

- `agents/` e `resources/` são embutidos dentro de cada skill, porque os `SKILL.md` do EGM referenciam esses caminhos relativos à raiz do plugin.
- `disable-model-invocation: true` é removido das skills `egm-*`; sem isso elas ficam fora do catálogo do modelo e o pipeline não inicia.

## Rota gratuita (OpenRouter)

O patch declara a rota `openrouter` restrita ao tier `:free`. Modelos autorizados: `nemotron-3.5-super-vl`,
`nemotron-3-ultra-550b-a55b`, `nemotron-3-nano-omni-30b-a3b-reasoning` e `north-mini-code`.

Ids do catálogo embutido podem já ter virado pagos (404) ou estar limitados (429). Antes de confiar, teste:

```powershell
$key = (Get-Content "$HOME\.dsh\.env" | Select-String 'OPENROUTER_API_KEY=(.+)').Matches[0].Groups[1].Value
Invoke-RestMethod -Method Post -Uri 'https://openrouter.ai/api/v1/chat/completions' `
  -Headers @{ Authorization = "Bearer $key" } -ContentType 'application/json' `
  -Body '{"model":"nvidia/nemotron-3.5-super-vl:free","messages":[{"role":"user","content":"ok"}],"max_tokens":50}'
```

Para trocar de modelo: marque outra opção em Plugins → Subagente e salve — o harness reescreve `allowedModels` no patch sozinho.

## Pré-requisitos

- DeepSeek Harness instalado (o `install.ps1` espera o layout `~/.dsh`).
- Python embutido do harness para `consultar-leis` (o `rodar.cmd` já aponta para `~/.dsh/dsh-runtimes/.../python.exe`).
- Acervo de leis em `H:\acervo\leis` ou `DSH_LEIS_ACERVO`.

## Aviso

Este diretório versiona configuração, não segredos. `.env` e `.credentials.yaml` estão no `.gitignore`.
