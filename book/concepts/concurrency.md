# Concurrency

## Problems

### Data race / race condition

!!! info "AI-generated"

A **data race** occurs when concurrent operations access the same memory, at least
one operation writes, and the accesses are not ordered by the language's
synchronization rules. A **race condition** is broader: correctness depends on
uncontrolled timing or ordering even when every individual access is atomic.

### Deadlock

2 or more tasks waiting for a shared resource, that must be free from the other, so none of them will get the resource -> indefinite blocking.

- Happens when following 4 happen simultaneously (Coffman’s conditions):
  - Mutual exclusion. -> only one task allowed.
  - Hold and wait condition. -> a task has mutex on a resource and is requesting mutex on another resource.
  - No pre-emption. -> resource can only be released by the tasks that holds them.
  - Circular wait. -> (1 —> 2 —> 3 —> … n —> 1)

### Live lock

!!! info "AI-generated"

Two or more tasks keep reacting to one another and changing state, but no task
makes useful progress. Unlike a deadlock, the tasks remain active.

### Resource starvation

!!! info "AI-generated"

One task waits indefinitely because other tasks repeatedly receive the resource
or scheduling opportunity first.

- Solution -> fair allocation algorithm.
- Fairness solutions to this problem takes additional overhead.

### Priority Inversion

Low priority task holds the resource needed by the high priority task.

## Models

### Shared mutable state

!!! info "AI-generated"

- Synchronize/lock access - may lead to deadlocks
  - Fix deadlocks by locking objects in a pre-defined order.
- Use atomic operations for simple state transitions; use locks or higher-level
  coordination when several values must change together.
- Accidental Non-determinism in thread execution (coz controlled by OS).
  - Not evident from library/classes that they share mutable state.

### Functional way (parallelism)

!!! info "AI-generated"

Pure functions and immutable values reduce coordination because concurrent tasks
do not mutate the same state. They do not guarantee parallel speed-up or freedom
from deadlock; futures can still wait cyclically, block a limited executor, or
perform nondeterministic I/O.

- A **future** represents a result that may become available later.
- A **promise** is a writable handle used to complete a future once.
- Parallel work is useful only when the tasks are independent enough and the
  scheduling/communication overhead is smaller than the saved computation time.

### Message passing and functional concurrency

!!! info "AI-generated"

- **Clojure atoms** apply an atomic function to one reference. The function may
  be retried, so it must not perform side effects.
- **Clojure refs/STM** coordinate changes to multiple references inside `dosync`.
- **Clojure agents** serialize asynchronous actions against one value; `await`
  waits for queued actions when a synchronous boundary is needed.
- In the **actor model**, actors isolate state and communicate through messages.
  An actor handles one message at a time, but the system still needs supervision,
  mailbox limits, ordering assumptions, and failure handling.
