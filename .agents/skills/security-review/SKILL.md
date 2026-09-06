---
description: Reviews code changes for security vulnerabilities, authentication gaps, and injection risks
disable-model-invocation: true
argument-hint: <branch-or-path>
---

## Diff to review

!`git diff $ARGUMENTS`

Audit the changes above for:

1. **Injection vulnerabilities** (SQL, XSS, command injection)
2. **Authentication and authorization gaps** (missing auth checks, privilege escalation)
3. **Hardcoded secrets or credentials** (API keys, passwords, tokens in source)
4. **Insecure dependencies** (known CVEs in package references)
5. **Data exposure** (PII in logs, overly broad API responses)

Use `checklist.md` in this skill directory for the full review checklist.

Report findings with severity ratings (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) and concrete remediation steps for each finding.
