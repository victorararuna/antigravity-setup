<#
.SYNOPSIS
Instala o kit DSH (skills, personas, regras, mapa de modelos e patch de perfil) em ~/.dsh.

.DESCRIPTION
Complementa o install.ps1 da raiz, que instala o pacote em ~/.gemini/config para o Antigravity.
Este instala a variante adaptada para o DeepSeek Harness.

.PARAMETER NoProfile
Não sobrescreve ~/.dsh/profiles/desktop/cordis.patch.yml (mantém o perfil atual).
#>
[CmdletBinding()]
param(
    [switch]$NoProfile
)

$ErrorActionPreference = 'Stop'

$RepoDir   = Split-Path -Parent $PSScriptRoot
$DshHome   = Join-Path $HOME '.dsh'
$SkillsDst = Join-Path $DshHome 'skills'
$KitDst    = Join-Path $DshHome 'kit'
$utf8      = New-Object System.Text.UTF8Encoding($false)

New-Item -ItemType Directory -Force -Path $SkillsDst, $KitDst | Out-Null

function Install-SkillBundle {
    param([string]$Source, [string]$Name)
    $dst = Join-Path $SkillsDst $Name
    if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
    Copy-Item $Source $dst -Recurse -Force
    return $dst
}

Write-Host '== Skills avulsas ==' -ForegroundColor Cyan
foreach ($s in @('consultar-leis', 'unslop')) {
    $src = Join-Path $RepoDir "skills\$s"
    if (Test-Path $src) { Install-SkillBundle $src $s | Out-Null; Write-Host "  $s" }
}

Write-Host '== EGM: skills + personas + padrões ==' -ForegroundColor Cyan
$egm = Join-Path $RepoDir 'plugins\egm'
if (Test-Path $egm) {
    foreach ($dir in Get-ChildItem (Join-Path $egm 'skills') -Directory) {
        $dst = Install-SkillBundle $dir.FullName $dir.Name
        Copy-Item (Join-Path $egm 'agents')    (Join-Path $dst 'agents')    -Recurse -Force
        Copy-Item (Join-Path $egm 'resources') (Join-Path $dst 'resources') -Recurse -Force
        Write-Host "  $($dir.Name)"
    }
}

Write-Host '== peticionar-egm ==' -ForegroundColor Cyan
$pet = Join-Path $RepoDir 'plugins\peticionar-egm'
if (Test-Path $pet) {
    $dst = Install-SkillBundle (Join-Path $pet 'skills\peticionar-egm') 'peticionar-egm'
    Copy-Item (Join-Path $pet 'agents') (Join-Path $dst 'agents') -Recurse -Force
    Write-Host '  peticionar-egm'
}

Write-Host '== Liberando skills EGM para o modelo ==' -ForegroundColor Cyan
Get-ChildItem $SkillsDst -Directory | ForEach-Object {
    $f = Join-Path $_.FullName 'SKILL.md'
    if (-not (Test-Path $f)) { return }
    $text = [System.IO.File]::ReadAllText($f)
    if ($text -match '(?m)^disable-model-invocation:\s*true\s*$') {
        $new = [regex]::Replace($text, '(?m)^disable-model-invocation:\s*true\s*\r?\n', '')
        [System.IO.File]::WriteAllText($f, $new, $utf8)
        Write-Host "  $($_.Name)"
    }
}

Write-Host '== Regras, kit arquivado e mapa de modelos ==' -ForegroundColor Cyan
foreach ($name in @('AGENTS.md', 'egm-models.md')) {
    $src = Join-Path $PSScriptRoot $name
    if (Test-Path $src) { Copy-Item $src (Join-Path $DshHome $name) -Force; Write-Host "  $name" }
}
foreach ($p in @('canva', 'gdocs', 'gmail', 'gslides')) {
    $src = Join-Path $RepoDir "plugins\$p"
    if (Test-Path $src) {
        $dst = Join-Path $KitDst $p
        if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
        Copy-Item $src $dst -Recurse -Force
    }
}
$rules = Join-Path $RepoDir 'rules'
if (Test-Path $rules) {
    $dst = Join-Path $KitDst 'rules'
    if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
    Copy-Item $rules $dst -Recurse -Force
}

if (-not $NoProfile) {
    Write-Host '== Patch do perfil (rota free + política) ==' -ForegroundColor Cyan
    $profileDir = Join-Path $DshHome 'profiles\desktop'
    New-Item -ItemType Directory -Force -Path $profileDir | Out-Null
    $target = Join-Path $profileDir 'cordis.patch.yml'
    $source = Join-Path $PSScriptRoot 'profile\cordis.patch.yml'
    if (Test-Path $target) {
        Copy-Item $target "$target.bak" -Force
        Write-Host "  backup: $target.bak"
    }
    Copy-Item $source $target -Force
    Write-Host '  aplicado'
}

$envFile = Join-Path $DshHome '.env'
if (-not (Test-Path $envFile)) {
    [System.IO.File]::WriteAllText($envFile, "OPENROUTER_API_KEY=`n", $utf8)
    Write-Host "Criado $envFile — cole sua chave de https://openrouter.ai/keys" -ForegroundColor Yellow
}

Write-Host ''
Write-Host "Kit DSH instalado em $DshHome" -ForegroundColor Green
Write-Host 'Próximos passos:' -ForegroundColor Green
Write-Host '  1. Preencher OPENROUTER_API_KEY em ~/.dsh/.env'
Write-Host '  2. Reiniciar o DeepSeek Harness (o patch só é lido no boot)'
Write-Host '  3. Plugins -> Subagente: ligar a seleção de modelo, marcar as rotas e Salvar'
Write-Host '  4. A política vale apenas para sessões novas'
