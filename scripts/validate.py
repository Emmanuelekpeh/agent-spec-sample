"""Validate the example process records against schema/process.schema.json.

Run:  python scripts/validate.py
Exit code 0 = every record is structurally valid.
"""

import json
import pathlib
import sys

try:
    import jsonschema
except ImportError:
    sys.exit("jsonschema is required:  pip install jsonschema")

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "process.schema.json"
EXAMPLES = ROOT / "examples"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)

    failures = 0
    checked = 0
    for path in sorted(EXAMPLES.glob("*.json")):
        checked += 1
        record = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
        if errors:
            failures += 1
            print(f"FAIL {path.name}")
            for err in errors:
                location = "/".join(str(p) for p in err.path) or "<root>"
                print(f"     {location}: {err.message}")
        else:
            sourced = sum(1 for s in record.get("steps", []) if s.get("source_id"))
            total = len(record.get("steps", []))
            print(f"ok   {path.name}  status={record['status']}  "
                  f"steps={total}  sourced={sourced}/{total}  gaps={len(record.get('gaps', []))}")

    print(f"\n{checked - failures}/{checked} records valid")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
