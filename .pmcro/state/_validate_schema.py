import json, yaml

schema_path = "plugins/pmcro-marketplace-directory/skills/scaffold-skill/assets/schemas/scaffold-spec.schema.json"
with open(schema_path, encoding="utf-8") as f:
    schema = json.load(f)
print("schema JSON parses OK, top-level keys:", list(schema.keys()))

with open("examples/generative-domain-agent.spec.yaml", encoding="utf-8") as f:
    example = yaml.safe_load(f)

try:
    import jsonschema
    jsonschema.validate(instance=example, schema=schema)
    print("jsonschema.validate: example spec is VALID against the new schema")
except ImportError:
    print("jsonschema library not installed - skipping direct schema validation (schema JSON syntax already confirmed valid)")
except Exception as exc:
    print("jsonschema.validate FAILED:", exc)
