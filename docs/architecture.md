# Architecture and trust boundaries

Inspection only. The repository-wide disclaimer in the README applies here.

```mermaid
flowchart LR
    R[Developer request] --> A[Existing AI coding agent]
    A --> D[Discover pattern]
    D --> P[Select parameters]
    P --> V[Validate schema and parameters]
    V --> T[Render explicit templates]
    T --> G[Plan paths and detect conflicts]
    G --> O[In-memory proposal]
    O --> H[Human review]
```

The agent makes domain decisions. The catalogue performs case-insensitive keyword matching; it does not infer architecture. Definitions supply explicit source/destination pairs. The renderer reads declared templates and returns text. The planner validates rendered destinations before returning the complete proposal. No apply phase is provided.

## Trust model

Parameters, manifests, schemas, templates and generated source are untrusted illustrative material. YAML safe loading avoids object construction. JSON Schema draft 2020-12 checks contracts; only fragment-local references are admitted. Strict Jinja variables expose omissions; a sandbox, cleared globals and no loader reduce capabilities. These controls are not established security boundaries.

Source/schema paths are resolved under each pattern directory; manifest paths remain under the catalogue root. Proposed output paths must be relative, portable and contained in the intended output root after symlink resolution. Duplicate resolved destinations and occupied paths cause a planning error. Existing file ancestors are rejected. All proposals are collected in memory; no partial writes can occur because there is no writer.

There are no size, recursion, time or memory limits. Catalogue discovery is recursive. Reads and containment checks can race with filesystem changes. Schema keywords and template expressions can be computationally expensive. A hostile local filesystem or pattern library is outside this sketch's protection. Pattern provenance, immutable snapshots, resource isolation and a formal review process would be prerequisites for a future implementation.

## Determinism and errors

With identical template bytes, parameter values and dependency behaviour, rendering aims to reproduce the same text. This is not a cross-version reproducibility guarantee; dependencies are not locked. `DefinitionError` describes catalogue/schema/template problems; `ParameterError` describes invalid arguments; `PlanningError` describes destination problems. The CLI maps these to a JSON error and a nonzero status in its illustrative implementation.

An eventual write phase would require a separate design for atomicity, overwrite consent, symlink races and rollback. Preview checks cannot safely authorise later writes.
