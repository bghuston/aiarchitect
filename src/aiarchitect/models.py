"""Internal proposal models; no filesystem mutation."""
from dataclasses import dataclass
from pathlib import Path


class DefinitionError(ValueError):
    """A pattern definition, template or schema is malformed."""


class ParameterError(ValueError):
    """A caller supplied parameters outside the pattern contract."""


class PlanningError(ValueError):
    """A proposed destination is unsafe, duplicated or already occupied."""


@dataclass(frozen=True)
class TemplateDefinition:
    source: str
    destination: str


@dataclass(frozen=True)
class Pattern:
    id: str
    version: str
    description: str
    tags: tuple[str, ...]
    root: Path
    schema_path: Path
    templates: tuple[TemplateDefinition, ...]


@dataclass(frozen=True)
class GeneratedFile:
    path: Path
    content: str


def contained_path(root: Path, relative: str) -> Path:
    """Resolve a portable relative path and reject existing symlink escapes.

    This preview-time check is not a race-safe authorisation for later writes.
    """
    from pathlib import PurePosixPath
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or ".." in path.parts
            or "\\" in relative or ":" in relative or str(path) == "."):
        raise ValueError(f"Not a portable relative file path: {relative!r}")
    base = root.resolve()
    candidate = (base / path).resolve()
    if not candidate.is_relative_to(base) or candidate == base:
        raise ValueError(f"Path escapes root: {relative!r}")
    return candidate
