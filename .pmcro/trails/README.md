# trails

Class-B durable evidence products.

Each cycle owns a GUID-named folder:

```text
.pmcro/trails/<guid>/
  orchestrate.jsonl
  plan.jsonl
  make.jsonl
  check.jsonl
  reflect.jsonl
  disposition.json
```

- Every line in a phase JSONL is an instance of the trail-frame schema.
- Only the owning role appends to its phase file.
- Only the Reflector may write `disposition.json` and seal the trail.
- Sealed trails are immutable. Corrections start a new trail that may reference the prior one.
