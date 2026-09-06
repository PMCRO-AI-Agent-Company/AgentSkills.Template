Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make_da5d.jsonl | ForEach-Object {
    $_ | python .pmcro\runtime\trail_runtime.py make --trail da5d571d-876a-48be-9550-a5dedc01627f
}
Get-Content -Raw .pmcro\state\_frame_check_da5d.json | python .pmcro\runtime\trail_runtime.py check --trail da5d571d-876a-48be-9550-a5dedc01627f
