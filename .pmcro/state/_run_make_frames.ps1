Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Get-Content .pmcro\state\_frame_make3_0fa03edc.jsonl | ForEach-Object {
    $line = $_
    $line | python .pmcro\runtime\trail_runtime.py make --trail 0fa03edc-68e8-4357-9fa9-9d75a9360115
}
