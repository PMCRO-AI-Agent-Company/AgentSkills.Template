---
paths:
  - "src/api/**/*.cs"
  - "src/api/**/*.ts"
  - "plugins/**/*.cs"
---

# API Design Rules

- All endpoints must validate input with a schema validator (FluentValidation or Zod)
- Return shape: `{ data: T } | { error: string }` — never throw raw exceptions to callers
- Rate limit all public endpoints
- Every skill output frame must be a structured record (PlanFrame, MakeStep, CheckFrame, ReflectFrame)
- Async methods must include `CancellationToken ct` as the last parameter
- Do not expose internal stack traces in error responses
