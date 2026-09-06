Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
Remove-Item plugins\pmcro-marketplace-directory\skills\scaffold-skill\scripts\_upgrade_generator.py -Force
Remove-Item plugins\pmcro-marketplace-directory\skills\scaffold-skill\scripts\_upgrade_generator.ps1 -Force
Remove-Item plugins\pmcro-marketplace-directory\skills\scaffold-skill\scripts\run_upgrade.ps1 -Force
Remove-Item .pmcro\state\_scratch_render -Recurse -Force
Get-ChildItem plugins\pmcro-marketplace-directory\skills\scaffold-skill\scripts
