Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template\artifacts\claude-export-f58ab584\extracted'
Write-Host '=== files in conversations/ ==='
Get-ChildItem conversations -Recurse -File | ForEach-Object { "$($_.FullName) ($($_.Length) bytes)" }

Write-Host ''
Write-Host '=== searching for ROUNDTABLE ==='
$files = Get-ChildItem conversations -Recurse -File -Include *.json
$hits = Select-String -Path $files -Pattern 'roundtable' -SimpleMatch -CaseSensitive:$false
Write-Host "Match count: $($hits.Count)"
$hits | Select-Object -First 5 | ForEach-Object { "$($_.Path): ...$($_.Line.Substring([Math]::Max(0,$_.LineNumber-1)))..." }

Write-Host ''
Write-Host '=== searching for TRAIL PLAYER ==='
$hits2 = Select-String -Path $files -Pattern 'trail.?player' -CaseSensitive:$false
Write-Host "Match count: $($hits2.Count)"
