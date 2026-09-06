Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Remove-Item .pmcro\state\_scratch_omode_rt -Recurse -Force -ErrorAction SilentlyContinue

$files = Get-ChildItem -Recurse -Include *.md,*.json,*.yaml,*.yml,*.py -File | Where-Object {
    $_.FullName -notmatch '\\(\.git|\.vs|artifacts|node_modules|bin|obj)\\' -and
    $_.FullName -notmatch '\\\.pmcro\\trails\\' -and
    $_.FullName -notmatch '\\\.pmcro\\state\\'
}

Write-Host '=== remaining pmcro-reasoning-strategy hits (live, excl. trails/scratch) ==='
$hits1 = Select-String -Path $files -Pattern 'pmcro-reasoning-strategy' -SimpleMatch
$hits1 | Group-Object Path | ForEach-Object { "$($_.Count)`t$($_.Name)" }
if (-not $hits1) { Write-Host '(none)' }

Write-Host ''
Write-Host '=== remaining plugins/pmcro-csuite/omode hits (live, excl. trails/scratch) ==='
$hits2 = Select-String -Path $files -Pattern 'plugins/pmcro-csuite/omode' -SimpleMatch
$hits2 | Group-Object Path | ForEach-Object { "$($_.Count)`t$($_.Name)" }
if (-not $hits2) { Write-Host '(none)' }

Write-Host ''
Write-Host '=== old directory still exists? ==='
Test-Path plugins\pmcro-reasoning-strategy
Test-Path plugins\pmcro-csuite\omode
