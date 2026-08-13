# Concurrency in Go

## Intro

- Golang binary includes machine code + "GC" + "Scheduler".
- There is no runtime like JVM.
- In Go application, Built-in "Scheduler" is the entry-point instead of main() function, scheduler in-turn executes the main() function.
- Scheduler takes care of borrowing Threads from OS.
- Instruction which are handed to the scheduler to execute are called "go-routines" ( "Managed Concurrency" ).
  - bare minimum OS thread (in Linux) takes ~ 2 MB memory
  - bare minimum go-routine takes ~ 2 KB memory  (it was 8 earlier, then became 4 and now it is 2 KB)
- Concurrency is built into the language instead of SDK / Library / API like Java etc.
  - "go" keyword
  - channel data type
  - channel operator ( <- )
  - range, select-case constructs

## Basic Constructs

### Wait Groups

```go
wg := sync.WaitGroup{}

func f1() {
    fmt.Println("f1 started")
    time.Sleep(1 * time.Seconds)
    fmt.Println("f1 stopped")

    wg.Done()
}

func f2() {
    fmt.Println("f2 started")
    time.Sleep(2 * time.Seconds)
    fmt.Println("f2 stopped")

    wg.Done()
}

func main() {
    wg.Add(1)

    go f1()
    f2()
    wg.Wait()
}
```

- Wait group detects the deadlock in case if all the the go-routines are in sleep state (non-runnable state).
- it is better to was WaitGroup ref as an arg to functions to be executed as go-routines.

### Managing State with Concurrency

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
    count++
    c.Unlock()
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

> "Communicate by sharing memory"

- We can Communicate by sharing memory
  - we can have common variable(s)
  - there are many challenges with this approach

> "Share memory by communicating"

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
- In case of streaming, on `close(ch)` the receiver will keep reading "zero" value (in a non-blocking manner) for the data-type.
  - To avoid this, we can use `data, isOpen := <- ch; isOpen { ... }`
  - Or, we can range over a channel like: `for data := range ch { ... }`

## Concurrency - Streaming

### Multiple Channels

### Buffered Channels

## Concurrency - Patterns

### Runner

### Pool

### Worker
