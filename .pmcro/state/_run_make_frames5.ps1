Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make_8cc3.jsonl | ForEach-Object {
    $_ | python .pmcro\runtime\trail_runtime.py make --trail 8cc37c30-cae3-4bb2-9b1c-235b5c1b74af
}
Get-Content -Raw .pmcro\state\_frame_check_8cc3.json | python .pmcro\runtime\trail_runtime.py check --trail 8cc37c30-cae3-4bb2-9b1c-235b5c1b74af
