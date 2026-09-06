Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make_74c3.jsonl | ForEach-Object {
    $_ | python .pmcro\runtime\trail_runtime.py make --trail 74c3922e-b508-47c2-9342-5a04a4d6643f
}
Get-Content -Raw .pmcro\state\_frame_check_74c3.json | python .pmcro\runtime\trail_runtime.py check --trail 74c3922e-b508-47c2-9342-5a04a4d6643f
