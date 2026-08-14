# Context

## What a context carries

!!! info "AI-generated"

`context.Context` carries a cancellation signal, deadline, and request-scoped
values across API boundaries. It is safe for use by multiple goroutines.

Use context for work lifetime, not as an optional-parameter bag. Pass it as the
first parameter, usually named `ctx`, and do not store it in a struct unless an
API specifically requires that pattern.

## Hierarchy

!!! info "AI-generated"

Derived contexts form a tree. Canceling a parent cancels every descendant, while
a child cannot cancel its parent.

~{Go context cancellation tree}(<go-context-tree.json> "Parent cancellation propagates to all descendants, while child cancellation stops only that subtree.")

```go
ctx, cancel := context.WithTimeout(parent, 2*time.Second)
defer cancel()

select {
case result := <-work(ctx):
    return result, nil
case <-ctx.Done():
    return Result{}, ctx.Err()
}
```

Call the returned cancel function even when the timeout does not fire; it releases
the associated timer and references promptly.

## Context - Applied

!!! info "AI-generated"

```go
func findUser(ctx context.Context, db *sql.DB, id int64) (User, error) {
    var user User
    err := db.QueryRowContext(
        ctx,
        `SELECT id, name FROM users WHERE id = ?`,
        id,
    ).Scan(&user.ID, &user.Name)
    return user, err
}
```

Use `WithValue` only for request-scoped metadata that crosses API boundaries,
such as a request ID. Use an unexported key type to avoid collisions. Required
business inputs should remain ordinary typed parameters.

Further reading: [Go context package](https://pkg.go.dev/context) and
[Go concurrency patterns: context](https://go.dev/blog/context).
