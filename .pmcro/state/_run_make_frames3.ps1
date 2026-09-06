Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make_dc6a.jsonl | ForEach-Object {
    $_ | python .pmcro\runtime\trail_runtime.py make --trail dc6a78dc-115c-4985-be5f-22afeb96895c
}
Get-Content -Raw .pmcro\state\_frame_check_dc6a.json | python .pmcro\runtime\trail_runtime.py check --trail dc6a78dc-115c-4985-be5f-22afeb96895c
