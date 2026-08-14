# Data Engineering

## What a data engineer builds

!!! info "AI-generated"

Data engineering turns raw data into dependable datasets while preserving meaning
from ingestion to the final report.

A typical data platform has these stages:

1. **Ingest** from databases, APIs, files, queues, or event streams.
2. **Store** raw data with enough history to replay or audit it.
3. **Transform** data into validated, documented models.
4. **Serve** those models to analytics, machine learning, and applications.
5. **Observe** freshness, volume, schema, lineage, cost, and failures.

~{Data engineering platform stages}(<data-engineering-pipeline.json> "Sources flow through ingestion, durable raw storage, transformation, and serving while observability spans every stage.")

## Batch and streaming

!!! info "AI-generated"

| Batch | Streaming |
|---|---|
| Processes a bounded collection | Processes an unbounded sequence of events |
| Usually simpler to replay and reason about | Usually offers lower latency |
| Fits periodic reports and backfills | Fits alerts, live features, and event-driven systems |

Many systems use both. A useful first question is not “Which technology is
newer?” but “How stale may this result be?” If hourly data is acceptable, a
batch job is often the calmer and cheaper design.

## Reliability checklist

!!! info "AI-generated"

- Make writes idempotent and plan replay/backfill paths.
- Define event time, time zone, and late-data behavior.
- Version schemas and data contracts.
- Test integrity and freshness; retain source lineage.
- Alert on user-visible loss or delay.

Further reading: [Apache Spark](./apache-spark.md) and [Big Data](./big-data.md).
