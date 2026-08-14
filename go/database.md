# Database Programming in Go

## `database/sql` mental model

!!! info "AI-generated"

`*sql.DB` is a concurrency-safe database handle and connection pool, not one
open connection. Create it once, configure pool limits, verify it with `Ping`,
and share it across handlers.

```go
db, err := sql.Open("driver-name", dsn)
if err != nil {
    return err
}
db.SetMaxOpenConns(20)
db.SetMaxIdleConns(10)
db.SetConnMaxLifetime(30 * time.Minute)

if err := db.PingContext(ctx); err != nil {
    return err
}
```

Import a driver separately. The standard library defines the common interface;
the driver implements the wire protocol.

## Querying safely

!!! info "AI-generated"

```go
rows, err := db.QueryContext(ctx,
    `SELECT id, name FROM users WHERE active = ?`, true)
if err != nil {
    return err
}
defer rows.Close()

for rows.Next() {
    var user User
    if err := rows.Scan(&user.ID, &user.Name); err != nil {
        return err
    }
}
return rows.Err()
```

Use placeholders and bound arguments rather than formatting user input into SQL.
Placeholder syntax differs by driver. Check both the query error and `rows.Err()`;
iteration can fail after returning some rows.

## Transactions

!!! info "AI-generated"

```go
tx, err := db.BeginTx(ctx, nil)
if err != nil {
    return err
}
defer tx.Rollback()

if _, err := tx.ExecContext(ctx, updateSQL, amount, accountID); err != nil {
    return err
}
return tx.Commit()
```

Use only the `*sql.Tx` methods inside the transaction. Calling `db` directly may
run on another connection and therefore outside that transaction. A deferred
rollback is harmless after a successful commit.

Further reading: [Accessing relational databases in Go](https://go.dev/doc/database/).
