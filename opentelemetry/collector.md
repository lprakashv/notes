# OpenTelemetry Collector

## Role

!!! info "AI-generated"

The OpenTelemetry Collector is a vendor-neutral service for receiving,
processing, and exporting telemetry. Applications can send one protocol and the
Collector can batch, filter, enrich, sample, and forward the data to one or more
backends.

A Collector does not store telemetry as its primary job. It is a pipeline
component, so design for backpressure, retries, queue limits, and what happens
when the destination is unavailable.

## Pipeline model

!!! info "AI-generated"

Each signal pipeline is assembled from three component types:

- **receivers** accept telemetry, for example OTLP;
- **processors** transform or buffer it, for example `batch` or `memory_limiter`;
- **exporters** send it to another Collector or backend.

~{OpenTelemetry Collector pipeline}(<opentelemetry-collector-pipeline.json> "Applications send telemetry through receivers and ordered processors to exporters and observability backends.")

```yaml
receivers:
  otlp:
    protocols:
      grpc: {}
      http: {}

processors:
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
  batch: {}

exporters:
  debug: {}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [debug]
```

Defining a component is not enough; it must also be referenced from a pipeline
under `service`.

## Deployment patterns

!!! info "AI-generated"

- **Agent:** one Collector near each workload or node; useful for host-local data.
- **Gateway:** a shared tier for central policy, sampling, and export.
- **Agent plus gateway:** local collection with centralized processing.

Start with the fewest moving parts that meet the reliability requirement. A
gateway needs horizontal scaling and load balancing for the protocol and any
stateful processors it uses.

Further reading: [Collector documentation](https://opentelemetry.io/docs/collector/)
and [configuration](https://opentelemetry.io/docs/collector/configuration/).
