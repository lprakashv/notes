# Concurrency

## Problems

### Data race / race condition

2 or more tasks writing a shared variable outside a critical section (without any synch mechanism) then the final output depends upon order of execution.

### Deadlock

2 or more tasks waiting for a shared resource, that must be free from the other, so none of them will get the resource -> indefinite blocking.

- Happens when following 4 happen simultaneously (Coffman’s conditions):
  - Mutual exclusion. -> only one task allowed.
  - Hold and wait condition. -> a task has mutex on a resource and is requesting mutex on another resource.
  - No pre-emption. -> resource can only be released by the tasks that holds them.
  - Circular wait. -> (1 —> 2 —> 3 —> … n —> 1)

### Live lock

2 tasks always changing states due to another actions of the other -> perpetually changing and not continuing their work.

### Resource starvation

More than one tasks waiting for the same resource, when it gets freed up is is allocated to one of them. One of the tasks might never get the resource

- Solution -> fair allocation algorithm.
- Fairness solutions to this problem takes additional overhead.

### Priority Inversion

Low priority task holds the resource needed by the high priority task.

## Models

### Shared mutable state

- Synchronize/lock access - may lead to deadlocks
  - Fix deadlocks by locking objects in a pre-defined order.
- Use atomic wherever necessary (better than custom synchronization).
- Accidental Non-determinism in thread execution (coz controlled by OS).
  - Not evident from library/classes that they share mutable state.

### Functional way (parallelism)

- Better concurrency support using pure functions.
- Basic primitives
  - __Futures__
    - Block of code running in a different thread.
    - Cannot have deadlocks.
    - Can make parallel execution with multiple processors.
    - Faster execution and deterministic results.
  - __Promises__
    - Container where we can put the value only once.
    - Will block the promise read until the promise gets filled.
    - Can have "deadlocks"!!
      - Predictable/deterministic.

### Functional concurrency

- __Atoms__ in clojure (atomic references)
  - More atomic swaps than the actual changes needed (rollback and discarding the inconsistent atomic change)
    - Solution: put more values in same atom
    - Solution: __STM__
- Agents
  - Same as atoms -> just the fn needed to update value runs on a diff thread.
  - Await needed at the end to wait for all the update ops on the agent.
- __Ref__ / __STM__
  - Unlike atom, can synchronize multiple values
  - Each operation should by in transaction (`dosync`)
- __Actor model__
