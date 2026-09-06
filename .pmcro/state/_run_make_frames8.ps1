Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make_260c.jsonl | ForEach-Object {
    $_ | python .pmcro\runtime\trail_runtime.py make --trail 260c4ce2-fc3e-4e76-883c-6a4e9b1869b7
}
Get-Content -Raw .pmcro\state\_frame_check_260c.json | python .pmcro\runtime\trail_runtime.py check --trail 260c4ce2-fc3e-4e76-883c-6a4e9b1869b7
