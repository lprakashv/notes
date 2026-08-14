# OpenTelemetry Logs

## What OpenTelemetry adds

!!! info "AI-generated"

OpenTelemetry defines a common log data model and a path for collecting,
processing, and exporting log records. It does not require replacing a mature
application logging library. Existing logs can be bridged or collected and then
translated into the OpenTelemetry model.

## Correlation

!!! info "AI-generated"

When a log is emitted during an active span, include the trace ID and span ID.
That lets an observability backend move from a log line to the request trace
without guessing from timestamps.

Useful fields include:

- event time and observed time;
- severity text and number;
- message body or structured event fields;
- service/resource attributes;
- trace ID, span ID, and trace flags;
- instrumentation scope.

Do not make every identifier a resource attribute. Resource attributes describe
the entity producing telemetry; request-specific values belong on each record.

## Collection patterns

!!! info "AI-generated"

1. **File/stdout collection:** an agent tails logs and parses them.
2. **Logging bridge/appender:** the application logging library emits records to
   OpenTelemetry.
3. **Direct API:** useful for structured events, but often less ergonomic than an
   established logging library.

Redact secrets before export, bound queues and retry buffers, and decide whether
the application should block or drop logs when the pipeline is unhealthy.

Further reading: [OpenTelemetry logging specification](https://opentelemetry.io/docs/specs/otel/logs/).
