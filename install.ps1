<#
.SYNOPSIS
Instala agentes, skills, plugins e regras do Antigravity em ~/.gemini/config.
#>
$ErrorActionPreference = "Stop"

$RepoDir = $PSScriptRoot
$TargetDir = Join-Path $HOME ".gemini\config"

$PluginsDst = Join-Path $TargetDir "plugins"
$SkillsDst  = Join-Path $TargetDir "skills"
$RulesDst   = Join-Path $TargetDir "rules"

New-Item -ItemType Directory -Force -Path $PluginsDst, $SkillsDst, $RulesDst | Out-Null

if (Test-Path (Join-Path $RepoDir "plugins")) {
    Get-ChildItem -Path (Join-Path $RepoDir "plugins") -Directory | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $PluginsDst -Recurse -Force
    }
}

if (Test-Path (Join-Path $RepoDir "skills")) {
    Get-ChildItem -Path (Join-Path $RepoDir "skills") -Directory | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $SkillsDst -Recurse -Force
    }
}

if (Test-Path (Join-Path $RepoDir "rules")) {
    Get-ChildItem -Path (Join-Path $RepoDir "rules") -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $RulesDst -Force
    }
}

Write-Host ""
Write-Host "Antigravity setup instalado com sucesso em: $TargetDir" -ForegroundColor Green
Write-Host "Componentes instalados:"
Write-Host "  - Plugins (17 agentes no total: 7 juridicos peticionar-egm + 10 egm; alem de canva, gdocs, gmail, gslides)"
Write-Host "  - Skills avulsas: consultar-leis, unslop"
Write-Host "  - Regras globais: nunca-cite-dispositivo-nao-lido.md"
Write-Host ""
Write-Host "Observacoes:"
Write-Host "  1. Para a skill consultar-leis, certifique-se de que o acervo esteja em H:\acervo\leis ou defina DSH_LEIS_ACERVO."
Write-Host "  2. Para os plugins Google Workspace (gdocs, gmail, gslides) e Canva, autentique suas contas no Gerenciador de Plugins do Antigravity."
