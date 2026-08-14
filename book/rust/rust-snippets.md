# Rust Snippets

## Ownership and borrowing

!!! info "AI-generated"

```rust
fn length(value: &str) -> usize {
    value.len()
}

fn main() {
    let name = String::from("Ferris");
    println!("{} has {} bytes", name, length(&name));
}
```

Passing `&name` borrows the value, so `main` keeps ownership. Use `&mut T` for
an exclusive mutable borrow; Rust permits either many immutable references or one
mutable reference at a time.

## `Option` and `Result`

!!! info "AI-generated"

```rust
fn first(items: &[String]) -> Option<&str> {
    items.first().map(String::as_str)
}

fn parse_port(raw: &str) -> Result<u16, std::num::ParseIntError> {
    raw.parse()
}
```

`Option<T>` represents a value that may be absent. `Result<T, E>` represents an
operation that may fail. Prefer matching or the `?` operator over `unwrap()` in
code that must handle bad input gracefully.

## Iterators

!!! info "AI-generated"

```rust
let even_squares: Vec<i32> = (1..=8)
    .filter(|n| n % 2 == 0)
    .map(|n| n * n)
    .collect();
```

Iterator adapters are lazy; `collect`, `sum`, and `for_each` are examples of
consumers that drive the iterator.

## Testing

!!! info "AI-generated"

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds_two_numbers() {
        assert_eq!(add(2, 3), 5);
    }
}
```

Run unit and integration tests with `cargo test`; use `cargo clippy` for common
correctness and style lints and `cargo fmt --check` in CI.
