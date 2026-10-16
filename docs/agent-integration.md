# Proposed agent interaction

Inspection only. All CLI signatures in the README are interface illustrations, not execution instructions.

An existing agent would first read compact catalogue metadata, then inspect a selected pattern's schema and output declarations. It would supply explicit parameters, receive validation diagnostics and request a generation proposal. A developer would review pattern fit, destination conflicts and domain logic before any future apply mechanism.

The current sketch has no model integration, subprocess adapter, installed CLI entry point, MCP server or agent skill. Paths are relative to the conceptual caller's working directory unless explicitly supplied. A catalogue is repository-local, not a network package registry.

Conceptual response shape (static illustration):

```json
{
  "previewOnly": true,
  "files": [{"path": "/illustrative/customer.entity.ts", "content": "..."}]
}
```

A future protocol could return a short manifest and content hashes, exposing file contents only when requested to avoid feeding boilerplate back into the agent context. It would need version pinning, bounded payloads, explicit error types and human-reviewed pattern provenance. No credentials are needed or proposed for this experiment.
