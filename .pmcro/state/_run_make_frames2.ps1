Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make_134d.jsonl | ForEach-Object {
    $_ | python .pmcro\runtime\trail_runtime.py make --trail 134d01f7-a633-43f2-bd29-043da659ff14
}
