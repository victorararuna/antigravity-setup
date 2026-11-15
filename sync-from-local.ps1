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

Write-Host "Sincronizacao concluida de $SourceDir para $RepoDir (auth.json removidos)." -ForegroundColor Cyan
git -C $RepoDir status -s
