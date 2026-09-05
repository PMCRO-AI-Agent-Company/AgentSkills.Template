# Reject Contract — scaffold-skill

The skill must refuse (and write nothing) when:

| Condition | Reason code |
|-----------|-------------|
| Spec fails JSON Schema validation | `schema-validation` |
| `id` or skill name contains placeholder tokens (`TODO`, `FIXME`, `xxx`, `changeme`, `placeholder`, `tbd`) | `placeholder-token` |
| Any path contains a drive letter (`P:\`, `C:\`) or absolute host path | `absolute-path` |
| Declared capability does not exist in the capability registry and is not explicitly marked planned | `unevidenced-capability` |
| Packaging target is unknown | `unknown-target` |
| Output path would escape the repository root | `path-escape` |

Refusal is a successful execution of the skill’s contract; it is not an error in the runtime sense. The caller receives a structured reject result.
