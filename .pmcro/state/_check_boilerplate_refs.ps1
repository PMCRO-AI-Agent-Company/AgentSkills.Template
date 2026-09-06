Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
$files = Get-ChildItem -Recurse -Include *.md,*.json,*.yaml,*.yml,*.py -File | Where-Object {
    $_.FullName -notmatch '\\(\.git|\.vs|artifacts|node_modules|bin|obj)\\' -and
    $_.FullName -notmatch '\\\.pmcro\\trails\\' -and
    $_.FullName -notmatch '\\\.pmcro\\state\\'
}
foreach ($term in @('code-reviewer', 'fix-issue', 'api-design', 'testing.md')) {
    Write-Host "=== $term ==="
    $hits = Select-String -Path $files -Pattern $term -SimpleMatch | Where-Object { $_.Path -notmatch '\\\.agents\\(agents|commands|rules)\\' }
    if ($hits) { $hits | ForEach-Object { "$($_.Path):$($_.LineNumber)" } } else { Write-Host '(no external references)' }
}
