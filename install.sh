#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/.gemini/config"

mkdir -p "$TARGET_DIR/plugins" "$TARGET_DIR/skills" "$TARGET_DIR/rules"

if [ -d "$REPO_DIR/plugins" ]; then
  cp -R "$REPO_DIR/plugins/." "$TARGET_DIR/plugins/"
fi

if [ -d "$REPO_DIR/skills" ]; then
  cp -R "$REPO_DIR/skills/." "$TARGET_DIR/skills/"
fi

if [ -d "$REPO_DIR/rules" ]; then
  cp -R "$REPO_DIR/rules/." "$TARGET_DIR/rules/"
fi

echo ""
echo "Antigravity setup instalado com sucesso em: $TARGET_DIR"
echo "Componentes instalados:"
echo "  - Plugins: peticionar-egm (7 agentes + skill), egm (10 agentes + 7 skills), canva, gdocs, gmail, gslides"
echo "  - Skills avulsas: consultar-leis, unslop"
echo "  - Regras globais: nunca-cite-dispositivo-nao-lido.md"
echo ""
echo "Observacoes:"
echo "  1. Para a skill consultar-leis, defina a variavel DSH_LEIS_ACERVO apontando para a pasta do acervo de leis."
echo "  2. Para os plugins Google Workspace (gdocs, gmail, gslides) e Canva, autentique suas contas no Antigravity."
