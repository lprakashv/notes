# HTTP in Go

## Minimal server

!!! info "AI-generated"

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /healthz", func(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
})

server := &http.Server{
    Addr:              ":8080",
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,
    IdleTimeout:       60 * time.Second,
}

if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
    log.Fatal(err)
}
```

Prefer an explicit `ServeMux` over global registration in reusable code. Configure
timeouts; an unbounded server can hold resources for slow or broken clients.

## Handler habits

!!! info "AI-generated"

- Read request-scoped cancellation from `r.Context()`.
- Set headers before calling `WriteHeader` or writing the body.
- Limit request bodies before decoding them.
- Reject unknown JSON fields when the API contract requires strict input.
- Return stable error shapes and do not expose internal error details.
- Put authentication, request IDs, logging, and recovery in middleware.

## Graceful shutdown

!!! info "AI-generated"

```go
ctx, stop := signal.NotifyContext(
    context.Background(), os.Interrupt, syscall.SIGTERM,
)
defer stop()

go func() {
    <-ctx.Done()
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    _ = server.Shutdown(shutdownCtx)
}()
```

`Shutdown` stops accepting new connections and waits for active handlers until
the deadline. The process still needs to handle the expected `http.ErrServerClosed`
result from `ListenAndServe`.

Further reading: [`net/http`](https://pkg.go.dev/net/http).
