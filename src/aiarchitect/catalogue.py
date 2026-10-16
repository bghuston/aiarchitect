"""Repository-local keyword discovery. Pattern files remain untrusted."""
from pathlib import Path
import re
import yaml
from .models import DefinitionError, Pattern, TemplateDefinition, contained_path


class PatternCatalogue:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def list_patterns(self) -> list[Pattern]:
        patterns: dict[str, Pattern] = {}
        try:
            for manifest in sorted(self.root.rglob("pattern.yaml")):
                if not manifest.resolve().is_relative_to(self.root):
                    raise DefinitionError("Manifest escapes catalogue")
                data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    raise DefinitionError(f"Expected a mapping: {manifest}")
                for key in ("id", "version", "description", "schema"):
                    if not isinstance(data.get(key), str) or not data[key].strip():
                        raise DefinitionError(f"Missing or malformed {key}: {manifest}")
                if not re.fullmatch(r"[a-z]+(?:\.[a-z]+)+", data["id"]):
                    raise DefinitionError("Pattern ID must be dotted lowercase words")
                tags = data.get("tags")
                entries = data.get("templates")
                if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
                    raise DefinitionError("tags must be a list of strings")
                if not isinstance(entries, list) or not entries:
                    raise DefinitionError("templates must be a nonempty list")
                definitions = []
                for entry in entries:
                    if not isinstance(entry, dict) or not all(
                        isinstance(entry.get(k), str) and entry[k]
                        for k in ("source", "destination")
                    ):
                        raise DefinitionError("Each template needs source and destination strings")
                    template_path = contained_path(manifest.parent, entry["source"])
                    if not template_path.is_file():
                        raise DefinitionError(f"Missing template: {entry['source']}")
                    definitions.append(TemplateDefinition(**entry))
                schema = contained_path(manifest.parent, data["schema"])
                if not schema.is_file():
                    raise DefinitionError("Missing schema")
                pattern = Pattern(data["id"], data["version"], data["description"],
                                  tuple(tags), manifest.parent, schema, tuple(definitions))
                if pattern.id in patterns:
                    raise DefinitionError(f"Duplicate pattern ID: {pattern.id}")
                patterns[pattern.id] = pattern
        except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
            raise DefinitionError(f"Invalid catalogue: {exc}") from exc
        return list(patterns.values())

    def search(self, query: str) -> list[Pattern]:
        words = query.casefold().split()
        return [p for p in self.list_patterns()
                if all(word in " ".join((p.id, p.description, *p.tags)).casefold()
                       for word in words)]

    def describe(self, pattern_id: str) -> Pattern:
        for pattern in self.list_patterns():
            if pattern.id == pattern_id:
                return pattern
        raise DefinitionError(f"Unknown pattern: {pattern_id}")
