# Proposed benchmark methodology

No benchmarks have been executed. Token savings, lower costs, faster completion and improved consistency remain hypotheses. This document is a study design, not an execution recommendation for this inspection-only repository.

## Paired comparison

Use matched tasks such as an audited entity, a transactional command and a module boundary. Hold repository snapshot, agent model/version, prompt, tool permissions, stopping criteria and quality requirements constant. Compare conventional generation with catalogue discovery plus parameter submission. Randomise order across repeated trials; separate cold-cache and warm-cache conditions. Include unsuccessful attempts rather than selecting successful examples.

Capture all input/output tokens (including catalogue retrieval, schemas, previews, corrections and retries), cached input tokens, tool calls, elapsed time and manual corrections. Compute API cost from recorded usage and dated provider rates. Do not equate fewer output tokens with lower total cost. Record template-authoring/review/maintenance effort separately and report amortisation across reuse counts.

Assess both outputs against the same independently defined behaviour tests and architectural rubric. Reviewers should be blinded to the approach where practical. Include test pass rate, architectural violations and manual correction effort; speed without acceptable quality is not a successful completion. Report task complexity, sample count, dispersion and failures alongside central estimates.

| Metric | Conventional AI | aiarchitect |
|---|---|---|
| Input tokens | To measure | To measure |
| Output tokens | To measure | To measure |
| Total API cost | To measure | To measure |
| Tool calls | To measure | To measure |
| Completion time | To measure | To measure |
| Test pass rate | To measure | To measure |
| Architectural violations | To measure | To measure |
| Manual corrections | To measure | To measure |

Potential confounders include prompt tuning, model caching, prior familiarity, catalogue search overhead, template maturity, generated content returned into context and how much novel logic each task contains. A useful outcome would identify break-even reuse counts and tasks where templates increase cost. Results would apply to the measured setup, not all agents or architectures.
