# Deliberate limitations

The exact inspection-only disclaimer in the README governs this repository. Code, illustrative tests, templates and sample outputs have not been executed or independently verified.

- Discovery is keyword-based, loads the catalogue afresh and has no semantic ranking.
- Schemas cover structural parameters and a small set of naming constraints, not domain correctness or every TypeScript identifier rule.
- Templates have no execution hooks or loader, but sandboxing does not prevent resource exhaustion or malicious generated source.
- Paths are checked for a preview only; filesystem races and safe application are unresolved.
- There is no write/apply command, merge policy, composition, rollback, provenance, pinning, migrations or architecture enforcement.
- Entity fields do not implement persistence semantics. CQRS transaction interfaces have no adapter. Module configuration is static and unresolved.
- Dependency metadata is not a reviewed lockfile. No production compatibility or supported environment is established.
- No agent integration, credentials, service, database, cloud deployment or functioning example application is provided.
- Sample tests describe intended boundary behaviour. Their presence does not demonstrate correctness or establish security.
- No token economics or performance claim has been measured.

The intended review activity is reading the narrative, contracts, templates and source to discuss architectural choices and their trade-offs.
