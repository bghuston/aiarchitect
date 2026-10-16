# Pattern contracts

Inspection only; definitions and outputs have not been executed or verified.

Each pattern has a dotted ID, metadata version, description, keyword tags, a local JSON Schema and explicit template source/destination declarations. Versioning is descriptive: there is no resolver, lockfile, compatibility policy or migration implementation. Unknown parameters are rejected. Boolean controls are required, so JSON Schema defaults are not mistaken for injected values.

| ID | Parameters | Proposed outputs |
|---|---|---|
| `database.entity` | PascalCase name, fields, auditable, softDelete | Lowercased name plus `.entity.ts` |
| `cqrs.command` | PascalCase name, aggregate, input, transactional | Lowercased name plus `.command.ts` |
| `project.module` | Lowercase kebab-case name | Layer README placeholders, index, tsconfig and package metadata |

Names are deliberately restricted. Field types are `string`, `number`, `boolean`, `datetime`; the latter maps to TypeScript `Date`. `required` omitted or false produces an optional property. Duplicate fields are rejected, as are entity fields shadowing standard identifiers/audit/deletion fields. The identifier subset is illustrative and does not implement every TypeScript naming rule. Lowercasing filenames is simple and can create collisions; the planner rejects existing destinations rather than merging them.

## Entity

Audit and deletion controls add fields only. Persistence adapters must allocate valid UUIDs, update timestamps and apply soft-delete filtering. There is no database schema, uniqueness enforcement or repository implementation.

## CQRS command

When `transactional` is true, the handler invokes the business extension point inside `UnitOfWork.withinTransaction`, passing the adapter's transaction scope. This expresses the intended boundary without inventing a database. Commit, rollback, nesting, retries and transaction-scoped repositories are not implemented. When false, the operation calls the extension point directly. Both variants throw until domain logic is supplied.

The supplied RegisterCustomer payload omits `required`, so `email` is optional in the illustration. A domain-specific registration pattern would normally demand it; callers must deliberately select the appropriate contract. No claim of valid customer registration follows from schema acceptance.

## Module

Layer placeholders document intended dependencies; they do not enforce them. The static TypeScript configuration demonstrates strict checking intentions and the private package metadata lists an illustrative TypeScript dependency. There are no scripts, working application or resolved dependencies. UI forms and other catalogue families are future ideas only.
