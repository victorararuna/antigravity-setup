# Antigravity Setup — Agentes, Skills, Plugins e Regras

Repositório centralizado para instalar rapidamente todos os meus agentes, skills, plugins e regras globais do Google Antigravity (`~/.gemini/config`) em qualquer estação de trabalho.

---

## Instalação em 1 comando

### Windows (PowerShell)

```powershell
git clone https://github.com/victorararuna/antigravity-setup.git "$HOME\antigravity-setup"; & "$HOME\antigravity-setup\install.ps1"
```

### Linux / macOS (Bash)

```bash
git clone https://github.com/victorararuna/antigravity-setup.git "$HOME/antigravity-setup" && bash "$HOME/antigravity-setup/install.sh"
```

---

## Inventário do Pacote

### 1. Plugins e Agentes (`plugins/`)

| Plugin | Descrição | Agentes incluídos | Skills incluídas |
| :--- | :--- | :--- | :--- |
| **`peticionar-egm`** | Orquestra 7 Goldfishes jurídicos isolados integrados à skill `consultar-leis` | `peticao-adversario`, `peticao-fatos-autos`, `peticao-juiz`, `peticao-jurisprudencia`, `peticao-legislacao`, `peticao-processual`, `peticao-revisor` | `peticionar-egm` |
| **`egm`** | Elephant-Goldfish Model para design, revisão de documentos, planos e código | `bootstrap_orchestrator`, `codebase_details`, `comprehension`, `design_critic`, `implementation_readiness`, `inventive_catalyst`, `structural`, `style`, `synthesizer`, `zoom_out` | `egm-bootstrap`, `egm-brainstorm`, `egm-draft`, `egm-drift-report`, `egm-resolve`, `egm-review`, `egm-review-loop` |
| **`canva`** | Integração e manipulação de designs Canva (MCP + skills) | — | `brand-check`, `bulk-create`, `cli`, `edit-design`, `get-design-feedback`, `implement-feedback`, `resize-for-social-media` (+ `inactive-skills`) |
| **`gdocs`** | Leitura, criação e edição de Google Docs | — | `gdocs` |
| **`gmail`** | Busca, leitura, rascunho e envio no Gmail | — | `gmail` |
| **`gslides`** | Leitura, criação e exportação no Google Slides | — | `gslides` |

### 2. Skills Avulsas (`skills/`)

- **`consultar-leis`**: Consulta de legislação brasileira em Markdown (`H:\acervo\leis`), verificação de vigência/redação e atuação como parecerista sênior ou análise judicial imparcial (`SKILL.md`, `references/atuacao.md`, `references/citacao.md`, `references/peticao.md`, `scripts/consultar.py`, `scripts/rodar.cmd`).
- **`unslop`**: Polimento e redesign de interfaces UI (`SKILL.md`, `agents/openai.yaml`, `references/`, `scripts/`).

### 3. Regras Globais (`rules/`)

- **`nunca-cite-dispositivo-nao-lido.md`**: Regra global que proíbe citar dispositivo legal, súmula, ato normativo ou precedente não lido diretamente no acervo (`H:\acervo\leis`) ou fonte oficial verificável.

### 4. DSH (DeepSeek Harness)

Variante adaptada para o DeepSeek Harness, em [`dsh/`](dsh/README.md): as skills com `agents/` e `resources/` embutidos, `AGENTS.md` global, mapa de modelos por persona (`egm-models.md`) e patch de perfil com a rota gratuita do OpenRouter.

```powershell
& "$HOME\antigravity-setup\dsh\install.ps1"
```

Instala em `~/.dsh` e **não** toca em `~/.gemini/config`. Segredos (`.env`, `.credentials.yaml`) ficam fora do versionamento.

---

## Como atualizar o repositório com novas customizações

Quando você criar ou editar novos agentes, skills ou regras na sua máquina local (`~/.gemini/config`), execute na pasta do repositório:

```powershell
.\sync-from-local.ps1
git add -A
git commit -m "chore: atualiza agentes e skills"
git push
```

O script `sync-from-local.ps1` copia os arquivos de `~/.gemini/config` para o repositório e remove automaticamente arquivos sensíveis (`auth.json`) antes do commit.

---

## Notas Pós-Instalação

1. **Skill `consultar-leis` e Acervo de Leis**: Por padrão, `scripts\rodar.cmd` aponta para `H:\acervo\leis`. Em outras estações de trabalho onde o acervo estiver em outro caminho, defina a variável de ambiente `DSH_LEIS_ACERVO` (consultada automaticamente por `scripts/consultar.py`) ou passe `--acervo <caminho>`.
2. **Plugins Google Workspace (`gdocs`, `gmail`, `gslides`) e Canva**: Por segurança, arquivos de credencial/OAuth (`auth.json`) e estados locais (`config.json`, `projects/`, `sidecars/`) não são versionados (`.gitignore`). Ao instalar em uma nova máquina, faça login normalmente nas contas pelo Gerenciador de Plugins do Antigravity.
