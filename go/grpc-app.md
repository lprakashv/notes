# gRPC in Go

## Overview

!!! info "AI-generated"

gRPC is a remote-procedure-call framework commonly used for typed service-to-
service APIs. A Protocol Buffers schema defines messages and service methods;
code generators create client and server bindings for supported languages.

gRPC typically uses HTTP/2 as its transport. HTTP/2 provides multiplexed streams,
header compression, and flow control. Server-Sent Events and sticky sessions are
not gRPC or HTTP/2 features.

Communication patterns:

- unary: one request and one response;
- server streaming: one request and a stream of responses;
- client streaming: a stream of requests and one response;
- bidirectional streaming: independent request and response streams.

## Minimal contract

!!! info "AI-generated"

```proto
syntax = "proto3";

package catalog.v1;

option go_package = "example.com/catalog/gen/catalog/v1;catalogv1";

service CatalogService {
  rpc GetProduct(GetProductRequest) returns (GetProductResponse);
}

message GetProductRequest {
  string id = 1;
}

message GetProductResponse {
  string id = 1;
  string name = 2;
}
```

Field numbers are part of the wire contract. Do not reuse a removed field number;
reserve it and its old name. Prefer additive changes, propagate deadlines through
`context.Context`, and map expected failures to appropriate gRPC status codes.

## Operational checklist

!!! info "AI-generated"

- Enable TLS and authenticate callers.
- Set client deadlines; a server cannot infer a useful business timeout.
- Retry only idempotent calls and use bounded backoff.
- Configure message-size limits intentionally.
- Export latency, status-code, and saturation metrics.
- Use health checking and graceful shutdown for rolling deployments.

Further reading: [gRPC concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
and [gRPC Go quick start](https://grpc.io/docs/languages/go/quickstart/).
