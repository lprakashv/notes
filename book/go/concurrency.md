# Concurrency in Go

## Intro

!!! info "AI-generated"

A Go executable includes a runtime with a garbage collector, goroutine scheduler,
and network poller. The runtime schedules many goroutines over a smaller or equal
number of operating-system threads and grows goroutine stacks as needed.

Goroutines are lightweight, but not free. Every goroutine should have a bounded
lifetime and an owner that can wait for or cancel it. The main language and
library tools are:

- the `go` statement to start a goroutine;
- channels and the `<-` operator for communication;
- `select` for coordinating channel operations and cancellation;
- `sync` and `sync/atomic` for shared-state synchronization;
- `context.Context` for cancellation and deadlines across API boundaries.

## Basic Constructs

### Wait Groups

!!! info "AI-generated"

```go
func f1(wg *sync.WaitGroup) {
    defer wg.Done()
    fmt.Println("f1 started")
    time.Sleep(1 * time.Second)
    fmt.Println("f1 stopped")
}

func f2(wg *sync.WaitGroup) {
    defer wg.Done()
    fmt.Println("f2 started")
    time.Sleep(2 * time.Second)
    fmt.Println("f2 stopped")
}

func main() {
    var wg sync.WaitGroup
    wg.Add(2)

    go f1(&wg)
    go f2(&wg)
    wg.Wait()
}
```

A `WaitGroup` counts work; it does not detect deadlocks. Call `Add` before starting
the goroutine and arrange for exactly one `Done` per unit. A `WaitGroup` must not
be copied after first use, so pass a pointer when it crosses a function boundary.

### Managing State with Concurrency

!!! info "AI-generated"

- "data-races" will happen on mutations happening in go-routines
  - "-race" flag/switch in go command : `go run -race {x}` shows if there are race conditions and result may not be correct.
  - we can have same `-race` flag in `go build` command as well but DO NOT USE THE BUILD FOR PRODUCTION as there may be some performance degradation.

We can use Mutexes

- we will have to `Lock()` and `Unlock` everytime!

Or, we can encapsulate our state

```go
type Counter struct {
    sync.Mutex
    count int
}

func (c *Counter) Inc() {
    c.Lock()
    defer c.Unlock()
    c.count++
}
```

Or, we can use `atomic` library

```go
var count int64
atomic.AddInt64(&count, 1)

var atomicCount atomic.Int64
atomicCount.Add(1)
```

#### Communication b/w Go-Routines

!!! info "AI-generated"

> Avoid communicating by sharing memory; share memory by communicating.

Channels

- Channels don't behave exactly like a "queue".
- It can be visualized as a "door".
- We can use channels for synchronization as well, we do not need to be dependent on Wait-Groups.
  - because of their blocking / non-blocking nature in certain scenarios of send and receive.

Declaration and Initialization:

- `var ch chan int; ch = make(chan int)`
- Or : `ch := make(chan int)`

Operations:

- Send: `ch <- {data}`
  - it is "blocked" until a receive operation is "initiated"
- Receive: `data := <- ch`
  - it is also a blocked until the data is sent through the channel
- Channel constraints:
  - receive only channel with `<-chan {type}`
  - send only channel with `chan<- {type}`
  - we can use these syntaxes at parameters of functions or return type of functions
  - e.g., `func Producer(...) <-chan int { ... }`
- After `close(ch)`, receives drain buffered values and then return the element
  type's zero value immediately with `ok == false`.
  - Detect this with `data, isOpen := <-ch`.
  - Or, we can range over a channel like: `for data := range ch { ... }`

The sender that owns the stream should close the channel. Closing is a broadcast
that no more values will arrive; it is not needed for garbage collection.

## Concurrency - Streaming

### Multiple Channels

!!! info "AI-generated"

Use `select` when a goroutine must wait on more than one channel:

```go
select {
case value := <-results:
    return value, nil
case <-ctx.Done():
    return Result{}, ctx.Err()
}
```

If several cases are ready, one is chosen pseudo-randomly. A `default` case makes
the operation non-blocking and can accidentally create a busy loop; use it only
when dropping or polling is intentional.

### Buffered Channels

!!! info "AI-generated"

```go
jobs := make(chan Job, 16)
```

A send blocks only while the buffer is full; a receive blocks while it is empty.
Buffers can absorb short bursts and decouple producer timing, but they do not fix
an indefinitely slower consumer. Choose capacity from a measured burst or
backpressure requirement, not as a substitute for flow control.

## Concurrency - Patterns

### Runner

!!! info "AI-generated"

A runner owns the lifetime of several goroutines. It starts them, cancels siblings
when one fails or the caller cancels, and waits for all of them before returning.
This keeps background work from leaking beyond its request or process owner.

### Pool

!!! info "AI-generated"

A worker pool bounds concurrency: start a fixed number of workers, send jobs over
a channel, close the jobs channel when production ends, and wait for workers.
Propagate cancellation so producers do not block forever after consumers stop.

### Worker

!!! info "AI-generated"

```go
func worker(ctx context.Context, jobs <-chan Job, results chan<- Result) {
    for {
        select {
        case <-ctx.Done():
            return
        case job, ok := <-jobs:
            if !ok {
                return
            }
            result := process(job)
            select {
            case results <- result:
            case <-ctx.Done():
                return
            }
        }
    }
}
```

The second `select` matters: cancellation must also unblock a worker that is
trying to publish a result after the receiver has gone away.
