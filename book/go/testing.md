# Testing in Go

## Table-driven tests

!!! info "AI-generated"

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {name: "positive", a: 2, b: 3, want: 5},
        {name: "negative", a: -2, b: 1, want: -1},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.want {
                t.Fatalf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

Tests live in files ending with `_test.go`; test functions start with `Test` and
accept `*testing.T`. Prefer small inputs that explain the behavior over a large
fixture that hides it.

## Commands

!!! info "AI-generated"

```bash
go test ./...
go test -race ./...
go test -coverprofile=cover.out ./...
go tool cover -html=cover.out
go test -run '^TestAdd$/negative$' ./path/to/package
```

Coverage shows which statements ran, not whether the assertions were meaningful.
Use the race detector in CI where its extra time and memory are acceptable.

## HTTP and cleanup helpers

!!! info "AI-generated"

Use `httptest.NewRecorder` for a handler in isolation and `httptest.NewServer`
when client behavior and the full HTTP stack matter. Register cleanup with
`t.Cleanup`; use `t.TempDir` for per-test files and `t.Setenv` for temporary
environment variables.

Call `t.Parallel()` only after checking that the test does not share mutable
state, fixed ports, process-wide configuration, or a database fixture with other
parallel tests.

Further reading: [`testing`](https://pkg.go.dev/testing) and
[`net/http/httptest`](https://pkg.go.dev/net/http/httptest).
