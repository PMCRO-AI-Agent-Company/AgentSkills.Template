Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
$seed = Get-Content -Raw .pmcro\state\_seed_declarative_upgrade.txt
python .pmcro\runtime\trail_runtime.py open --seed $seed --host pmcr-o
