Set-Location 'C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template'
git mv plugins\pmcro-reasoning-strategy plugins\pmcro-omode
git mv plugins\pmcro-csuite\omode plugins\pmcro-csuite\skills\select-reasoning-strategy\assets
Write-Host '---AFTER MOVE---'
Get-ChildItem plugins\pmcro-omode
Write-Host '---'
Get-ChildItem plugins\pmcro-csuite\skills\select-reasoning-strategy
