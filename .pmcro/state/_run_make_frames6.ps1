Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make_f117.jsonl | ForEach-Object {
    $_ | python .pmcro\runtime\trail_runtime.py make --trail f1171d29-9846-42ea-a2c0-3335f8b6d1bc
}
Get-Content -Raw .pmcro\state\_frame_check_f117.json | python .pmcro\runtime\trail_runtime.py check --trail f1171d29-9846-42ea-a2c0-3335f8b6d1bc
