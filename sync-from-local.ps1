<#
.SYNOPSIS
Sincroniza plugins, skills e regras de ~/.gemini/config para este repositorio Git.
#>
$ErrorActionPreference = "Stop"

$RepoDir = $PSScriptRoot
$SourceDir = Join-Path $HOME ".gemini\config"

$PluginsSrc = Join-Path $SourceDir "plugins"
$SkillsSrc  = Join-Path $SourceDir "skills"
$RulesSrc   = Join-Path $SourceDir "rules"

$PluginsDst = Join-Path $RepoDir "plugins"
$SkillsDst  = Join-Path $RepoDir "skills"
$RulesDst   = Join-Path $RepoDir "rules"

New-Item -ItemType Directory -Force -Path $PluginsDst, $SkillsDst, $RulesDst | Out-Null

if (Test-Path $PluginsSrc) {
    Get-ChildItem -Path $PluginsSrc -Directory | ForEach-Object {
        $destPlugin = Join-Path $PluginsDst $_.Name
        if (Test-Path $destPlugin) { Remove-Item -Recurse -Force $destPlugin }
        Copy-Item -Path $_.FullName -Destination $PluginsDst -Recurse -Force
    }
    Get-ChildItem -Path $PluginsDst -Filter "auth.json" -Recurse -Force | Remove-Item -Force
    Get-ChildItem -Path $PluginsDst -Filter ".git" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
}

if (Test-Path $SkillsSrc) {
    Get-ChildItem -Path $SkillsSrc -Directory | ForEach-Object {
        $destSkill = Join-Path $SkillsDst $_.Name
        if (Test-Path $destSkill) { Remove-Item -Recurse -Force $destSkill }
        Copy-Item -Path $_.FullName -Destination $SkillsDst -Recurse -Force
    }
    Get-ChildItem -Path $SkillsDst -Filter ".git" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
}

if (Test-Path $RulesSrc) {
    Get-ChildItem -Path $RulesSrc -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $RulesDst -Force
    }
}

# DSH (DeepSeek Harness): apenas configuracao. Nunca skills (elas carregam copias de
# agents/resources embutidos) nem credenciais (.env, .credentials.yaml).
$DshSrc = Join-Path $HOME ".dsh"
$DshDst = Join-Path $RepoDir "dsh"
if (Test-Path $DshSrc) {
    New-Item -ItemType Directory -Force -Path (Join-Path $DshDst "profile") | Out-Null
    foreach ($f in @("AGENTS.md", "egm-models.md")) {
        $s = Join-Path $DshSrc $f
        if (Test-Path $s) { Copy-Item $s (Join-Path $DshDst $f) -Force }
    }
    $dshPatch = Join-Path $DshSrc "profiles\desktop\cordis.patch.yml"
    if (Test-Path $dshPatch) { Copy-Item $dshPatch (Join-Path $DshDst "profile\cordis.patch.yml") -Force }
}

Write-Host "Sincronizacao concluida de $SourceDir e ~/.dsh para $RepoDir (auth.json e segredos removidos)." -ForegroundColor Cyan
git -C $RepoDir status -s
