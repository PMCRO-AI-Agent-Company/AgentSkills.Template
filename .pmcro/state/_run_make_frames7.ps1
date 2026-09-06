Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make_e5c0.jsonl | ForEach-Object {
    $_ | python .pmcro\runtime\trail_runtime.py make --trail e5c02321-82b0-4877-892f-49fbdee2f905
}
Get-Content -Raw .pmcro\state\_frame_check_e5c0.json | python .pmcro\runtime\trail_runtime.py check --trail e5c02321-82b0-4877-892f-49fbdee2f905
