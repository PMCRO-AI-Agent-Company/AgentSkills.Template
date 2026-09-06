Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
$files = Get-ChildItem -Recurse -Include *.md,*.json,*.yaml,*.yml -File | Where-Object {
    $_.FullName -notmatch '\\(\.git|\.vs|artifacts|node_modules|bin|obj)\\'
}
Write-Host '=== reasoning-strategy ==='
Select-String -Path $files -Pattern 'reasoning-strategy' -SimpleMatch |
    Group-Object Path | ForEach-Object { "$($_.Count)`t$($_.Name)" } | Sort-Object

Write-Host ''
Write-Host '=== omode (case-insensitive) ==='
Select-String -Path $files -Pattern 'omode' -SimpleMatch |
    Group-Object Path | ForEach-Object { "$($_.Count)`t$($_.Name)" } | Sort-Object
