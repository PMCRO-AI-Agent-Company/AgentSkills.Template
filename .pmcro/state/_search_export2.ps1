Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template\artifacts\claude-export-f58ab584\extracted'
$fileCount = (Get-ChildItem conversations -Recurse -File -Include *.json).Count
Write-Host "Total JSON files in conversations/: $fileCount"

$files = Get-ChildItem conversations -Recurse -File -Include *.json
$rtCount = 0
$tpCount = 0
$rtFiles = @()
$tpFiles = @()
foreach ($f in $files) {
    $text = [System.IO.File]::ReadAllText($f.FullName)
    if ($text -match '(?i)roundtable') { $rtCount++; $rtFiles += $f.Name }
    if ($text -match '(?i)trail.{0,3}player') { $tpCount++; $tpFiles += $f.Name }
}
Write-Host "Files containing 'roundtable': $rtCount"
Write-Host "Files containing 'trail player'-ish: $tpCount"
if ($rtFiles.Count -gt 0) { Write-Host "Roundtable files: $($rtFiles -join ', ')" }
if ($tpFiles.Count -gt 0) { Write-Host "Trail-player files: $($tpFiles -join ', ')" }
