# Databases

## Choosing a data model

!!! info "AI-generated"

Choose a database from the access patterns and guarantees the application needs,
not from the amount of data alone.

| Model | Good fit | Main trade-off |
|---|---|---|
| Relational | Transactions, joins, constraints, reporting | Schema changes need care |
| Document | Aggregate-shaped records with evolving fields | Cross-document constraints are harder |
| Key-value | Fast lookup by a known key | Limited ad-hoc querying |
| Wide-column | Large sparse datasets and predictable queries | Data is modeled around query paths |
| Graph | Relationship-heavy traversals | Operational and query-model complexity |
| Time-series | Metrics and timestamped observations | Specialized retention and query patterns |

“NoSQL” does not mean “no schema.” It usually means the schema is enforced by
application code, validation rules, or conventions instead of only by the
database engine.

## Transaction refresher

!!! info "AI-generated"

- **Atomicity:** a transaction commits completely or has no effect.
- **Consistency:** committed data satisfies the rules the database enforces.
- **Isolation:** concurrent transactions behave according to an isolation level;
  it does not imply that every transaction is fully serializable.
- **Durability:** acknowledged commits survive the failures covered by the
  database's durability configuration.

Isolation and replication are separate concerns. A strongly isolated local
transaction can still be replicated asynchronously, so a replica may briefly
return older data.

## Practical selection questions

!!! info "AI-generated"

1. What are the main reads and writes?
2. Which invariants must be atomic?
3. How stale may reads be?
4. What are the recovery objectives?
5. Can the team migrate, observe, back up, and restore it safely?

See [SQLite](./sqlite.md) for an embedded relational database.
