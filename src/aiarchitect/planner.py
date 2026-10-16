"""Preview only: no generated files are written."""
from pathlib import Path
from .models import GeneratedFile, Pattern, PlanningError, contained_path
from .renderer import Renderer


def plan(pattern: Pattern, params: dict, output_root: Path) -> list[GeneratedFile]:
    proposed = []
    seen: set[Path] = set()
    for destination, content in Renderer().render(pattern, params):
        try:
            path = contained_path(output_root, destination)
        except ValueError as exc:
            raise PlanningError(str(exc)) from exc
        # Lexical check also detects dangling symlinks at the destination.
        lexical = output_root / destination
        if path in seen or lexical.exists() or lexical.is_symlink():
            raise PlanningError(f"Duplicate or occupied destination: {destination}")
        # Existing file ancestors cannot contain generated children.
        if any(parent.exists() and not parent.is_dir() for parent in path.parents):
            raise PlanningError(f"Non-directory ancestor: {destination}")
        seen.add(path)
        proposed.append(GeneratedFile(path, content))
    return proposed
