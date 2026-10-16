"""Schema and parameter failures are distinct; no defaults are injected."""
import json
from jsonschema import Draft202012Validator, SchemaError
from .models import DefinitionError, ParameterError, Pattern


def load_schema(pattern: Pattern) -> dict:
    try:
        schema = json.loads(pattern.schema_path.read_text(encoding="utf-8"))
        if not isinstance(schema, dict):
            raise DefinitionError("Schema must be a JSON object")
        Draft202012Validator.check_schema(schema)
        # Only local definitions: no network reference resolution is intended.
        def check_refs(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in ("$ref", "$dynamicRef") and (
                        not isinstance(item, str) or not item.startswith("#")
                    ):
                        raise DefinitionError("Only fragment-local schema references are supported")
                    check_refs(item)
            elif isinstance(value, list):
                for item in value:
                    check_refs(item)
        check_refs(schema)
        return schema
    except (OSError, ValueError, SchemaError) as exc:
        raise DefinitionError(f"Invalid schema for {pattern.id}: {exc}") from exc


def validate_parameters(pattern: Pattern, params: dict) -> None:
    validator = Draft202012Validator(load_schema(pattern))
    errors = sorted(validator.iter_errors(params), key=lambda e: str(list(e.path)))
    if errors:
        details = [f"{'.'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors]
        raise ParameterError("; ".join(details))
    fields = params.get("fields", params.get("input", []))
    names = [field["name"] for field in fields]
    reserved = {"id", "createdAt", "updatedAt", "deletedAt"} if pattern.id == "database.entity" else set()
    if len(names) != len(set(names)) or reserved.intersection(names):
        raise ParameterError("Field names must be unique and must not shadow standard entity fields")
