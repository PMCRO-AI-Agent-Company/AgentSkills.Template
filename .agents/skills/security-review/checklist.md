# Security Review Checklist

## Input Validation
- [ ] All user input sanitized before DB queries
- [ ] File upload MIME types validated server-side
- [ ] Path traversal prevented on file operations
- [ ] Numeric bounds checked (no integer overflow)
- [ ] JSON deserialization uses allowlists, not open object graphs

## Authentication & Authorization
- [ ] Every endpoint has an explicit auth check (no implicit allow)
- [ ] JWT / API tokens expire appropriately (≤24h for user tokens)
- [ ] API keys stored in environment variables, never in source
- [ ] Passwords hashed with bcrypt or argon2 (no MD5/SHA1)
- [ ] RBAC enforced at the service layer, not just the UI

## Injection
- [ ] Parameterized queries used for all DB access
- [ ] Shell commands constructed with argument arrays, not string concatenation
- [ ] Template engines escape output by default; raw HTML only where explicitly safe
- [ ] XSS mitigated via Content-Security-Policy and output encoding

## Secrets & Credentials
- [ ] No secrets in committed files (check `.env`, `appsettings.json`, comments)
- [ ] Secret scanning CI gate passes (Gitleaks / TruffleHog)
- [ ] Key rotation procedure documented for all service credentials

## Dependencies
- [ ] `dotnet list package --vulnerable` returns no critical/high findings
- [ ] New NuGet / npm packages are pinned to a specific version
- [ ] License compatibility verified for new dependencies

## Logging & Observability
- [ ] PII not written to logs
- [ ] Error responses never expose stack traces to clients
- [ ] Structured logging used (no string interpolation in log calls)
