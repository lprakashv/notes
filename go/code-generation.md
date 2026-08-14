# Code Generation

## `go generate`

!!! info "AI-generated"

`go generate` runs commands declared by `//go:generate` directives. It is an
explicit developer tool: it is not run automatically by `go build`, `go test`,
or module download.

```go
package status

//go:generate stringer -type=State

type State int

const (
    Pending State = iota
    Running
    Done
)
```

Run every directive in the current package:

```bash
go generate
```

Run directives recursively for packages in the module:

```bash
go generate ./...
```

The generator executable must already be installed and available on `PATH`.

## Reproducible generation

!!! info "AI-generated"

- Pin generator versions in normal module tooling or a documented tool setup.
- Commit generated files when consumers should not need the generator.
- Put a “generated; do not edit” comment in generated output.
- Make generation deterministic; avoid timestamps and machine-specific paths.
- In CI, regenerate and fail if `git diff --exit-code` reports a change.
- Review generated code like dependency output: generators execute with the
  developer's permissions.

Further reading: [Generating code](https://go.dev/blog/generate).
