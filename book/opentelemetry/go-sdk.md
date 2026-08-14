# OpenTelemetry Go SDK

## Instrumentation layers

!!! info "AI-generated"

- The **API** is used by application and library instrumentation.
- The **SDK** samples, processes, and exports telemetry.
- **Instrumentation libraries** wrap common HTTP, database, and RPC packages.
- **Exporters** send telemetry through OTLP or another supported format.

Libraries should depend on the OpenTelemetry API and should not install a global
SDK. The application owns SDK configuration because it knows the deployment,
sampling, and export policy.

## Trace setup shape

!!! info "AI-generated"

```go
resource := resource.NewWithAttributes(
    semconv.SchemaURL,
    semconv.ServiceName("checkout"),
)

provider := sdktrace.NewTracerProvider(
    sdktrace.WithResource(resource),
    sdktrace.WithBatcher(exporter),
)
otel.SetTracerProvider(provider)
defer provider.Shutdown(context.Background())
```

Exporter construction and package paths vary by transport, so use the matching
current OTLP exporter documentation. Always call `Shutdown` with a bounded
context so buffered telemetry gets a chance to flush.

## Creating spans

!!! info "AI-generated"

```go
func loadOrder(ctx context.Context, id string) error {
    ctx, span := otel.Tracer("orders").Start(ctx, "load-order")
    defer span.End()

    span.SetAttributes(attribute.String("order.id", id))
    return queryOrder(ctx, id)
}
```

Pass `context.Context` through the call chain; it carries the current span. Avoid
high-cardinality values such as request IDs in metric attributes. As of the
official Go status page, traces and metrics are stable while logs remain beta,
so check status before adopting logs-specific APIs.

Further reading: [OpenTelemetry Go](https://opentelemetry.io/docs/languages/go/).
