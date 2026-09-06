Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
$files = Get-ChildItem -Recurse -Include *.md,*.json,*.yaml,*.yml,*.py -File | Where-Object {
    $_.FullName -notmatch '\\(\.git|\.vs|artifacts|node_modules|bin|obj)\\' -and
    $_.FullName -notmatch '\\\.pmcro\\trails\\' -and
    $_.FullName -notmatch '\\\.pmcro\\state\\'
}
foreach ($term in @('code-reviewer', 'fix-issue', 'api-design', 'rules/testing')) {
    Write-Host "=== $term ==="
    $hits = Select-String -Path $files -Pattern $term -SimpleMatch
    if ($hits) { $hits | ForEach-Object { "$($_.Path):$($_.LineNumber): $($_.Line.Trim())" } } else { Write-Host '(none)' }
}
