---
paths:
  - "**/*.test.ts"
  - "**/*.test.tsx"
  - "**/*.Tests.cs"
  - "**/*Tests.cs"
---

# Testing Rules

- Use descriptive test names: "should [expected] when [condition]"
- Mock external dependencies, not internal modules
- Clean up side effects in `afterEach` / `TearDown`
- One assertion per test where practical; group related assertions with `Assert.Multiple`
- Tests live next to source: `Foo.cs` → `Foo.Tests.cs`
- All skill tests must include an `eval.yaml` with at least one scenario
