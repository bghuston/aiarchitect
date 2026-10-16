"""Illustrative command contract; no installed entry point. Do not execute."""
import argparse
import json
from pathlib import Path
from .catalogue import PatternCatalogue
from .models import DefinitionError, ParameterError, PlanningError
from .planner import plan
from .validation import load_schema, validate_parameters


def metadata(pattern):
    return {"id": pattern.id, "version": pattern.version,
            "description": pattern.description, "tags": list(pattern.tags)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Inspection-only proposal interface")
    parser.add_argument("--catalogue", type=Path, default=Path("patterns"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    commands.add_parser("search").add_argument("query")
    commands.add_parser("describe").add_argument("id")
    for name in ("validate", "generate"):
        command = commands.add_parser(name)
        command.add_argument("id")
        command.add_argument("--params", type=Path, required=True)
        if name == "generate":
            command.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args(argv)
    catalogue = PatternCatalogue(args.catalogue)
    try:
        if args.command in ("list", "search"):
            patterns = catalogue.list_patterns() if args.command == "list" else catalogue.search(args.query)
            result = [metadata(p) for p in patterns]
        else:
            pattern = catalogue.describe(args.id)
            if args.command == "describe":
                result = {**metadata(pattern), "schema": load_schema(pattern),
                          "outputs": [t.destination for t in pattern.templates]}
            else:
                params = json.loads(args.params.read_text(encoding="utf-8"))
                validate_parameters(pattern, params)
                result = {"valid": True}
                if args.command == "generate":
                    result = {"previewOnly": True, "files": [
                        {"path": str(f.path), "content": f.content}
                        for f in plan(pattern, params, args.output_root)
                    ]}
        print(json.dumps(result, indent=2))
        return 0
    except (DefinitionError, ParameterError, PlanningError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
