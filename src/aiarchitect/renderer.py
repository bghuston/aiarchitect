"""Restricted rendering sketch. A sandbox is not resource isolation."""
from jinja2 import StrictUndefined, TemplateError
from jinja2.sandbox import SandboxedEnvironment
from .models import DefinitionError, Pattern, contained_path
from .validation import validate_parameters


class Renderer:
    def __init__(self):
        self.environment = SandboxedEnvironment(
            undefined=StrictUndefined, autoescape=False, keep_trailing_newline=True,
        )
        self.environment.globals.clear()
        # No loader, includes, executable hooks, custom objects or filesystem helpers.

    def render(self, pattern: Pattern, params: dict) -> list[tuple[str, str]]:
        validate_parameters(pattern, params)
        try:
            outputs = []
            for definition in pattern.templates:
                source = contained_path(pattern.root, definition.source)
                destination = self.environment.from_string(definition.destination).render(**params)
                content = self.environment.from_string(source.read_text(encoding="utf-8")).render(**params)
                outputs.append((destination, content))
            return outputs
        except (OSError, ValueError, TemplateError) as exc:
            raise DefinitionError(f"Cannot render {pattern.id}: {exc}") from exc
