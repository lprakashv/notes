# OpenTelemetry Metrics

## Instruments

!!! info "AI-generated"

Choose an instrument from what the value means:

| Instrument | Use |
|---|---|
| Counter | Monotonic totals such as completed requests |
| UpDownCounter | Values that may rise and fall, such as active jobs |
| Histogram | Distributions such as request duration or payload size |
| Observable Counter | A monotonic value read from another system |
| Observable UpDownCounter | A sampled value that may rise and fall |
| Observable Gauge | A current sampled measurement |

Record durations in a consistent unit and use semantic conventions when one
exists.

## Attributes and cardinality

!!! info "AI-generated"

Attributes split a metric into time series. A small bounded set such as HTTP
method or coarse status code is usually useful. User IDs, raw URLs, request IDs,
and timestamps can create an unbounded number of series and overwhelm the
pipeline.

Estimate cardinality before launch:

```text
series = instrument count × product of distinct attribute values
```

## Aggregation and temporality

!!! info "AI-generated"

The SDK aggregates measurements before export. A histogram keeps a count, sum,
and bucket counts rather than every observation. Exporters may use cumulative
temporality, where values cover the process lifetime, or delta temporality, where
values cover the interval since the previous export.

Metric readers and views control collection and aggregation. Keep views in
application-level telemetry configuration so libraries do not impose backend
policy.

Further reading: [OpenTelemetry metrics](https://opentelemetry.io/docs/concepts/signals/metrics/)
and [metrics data model](https://opentelemetry.io/docs/reference/specification/metrics/data-model/).
