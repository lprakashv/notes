# Java Multi-threading

## Java `Thread` class methods

### `Thread.currentThread()`

The return type of this method is Thread, it returns a reference of currently executing thread (who touched this method). It does not raise any exception.

### `long threadId()`

!!! info "AI-generated"

The thread ID is a positive `long` generated when the thread is created. It is
unique and unchanged during that thread's lifetime. `getId()` is deprecated since
Java 19; use `threadId()` in current code.

An ID is useful for diagnostics, not as a permanent application identity.

### `int getPriority()` and `void setPriority()`

The priority of thread can either be assigned by the JVM or by the programmer explicitly while creating the thread.

The thread's priority is in the range of 1 to 10. The __default priority of a thread is 5__.

### `Thread.State getState()`

!!! info "AI-generated"

Returns one of `NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, or
`TERMINATED`. The value is a snapshot intended for monitoring and diagnostics,
not for synchronization decisions.

### `void interrupt()`

An interrupt is an indication to a thread that it should stop what it is doing and do something else. It’s up to the programmer to decide exactly how a thread responds to an interrupt, but __it is very common for the thread to terminate__.

### `void join()`

This java thread join method puts the current thread on wait until the thread on which it’s called is dead. If the thread is interrupted, it throws `InterruptedException`.

If the referenced thread was __already terminated__ or __hasn’t been started__, the call to `join()` method returns __immediately__.

### `void run()`

The `run()` method of a thread encapsulates the logic that should be run by a thread.

### `void setDaemon(boolean on)`

!!! info "AI-generated"

Daemon status controls JVM shutdown; it does not mean low priority. JVM shutdown
begins after all started non-daemon threads terminate. Virtual threads are always
daemon threads.

The method `setDaemon()` can only be called after the Thread object has been created and the thread has not been started. An __attempt to call setDaemon() while a thread is running will throw an `IllegalThreadStateException`__.

### `Thread.sleep(long millis)`

`Thread.sleep()` the method can be used to pause the execution of the current thread for a specified time in milliseconds. The argument value for __milliseconds can't be negative__, else it throws `IllegalArgumentException`.

### `void start()`

When a program calls the `start()` method, a new thread is created, and then the `run()` method is executed.

We can't call the `start()` method twice; a second call throws
`IllegalThreadStateException`.

### `Thread.yield()`

!!! info "AI-generated"

`yield()` is only a hint that the current thread is willing to give up its current
use of a processor. The scheduler may ignore it, and the Java API does not promise
that another thread of a particular priority will run. It is rarely appropriate
outside diagnostics or concurrency-control implementation; verify any use with
profiling and tests.

---

## Thread Lifecycle

!!! info "AI-generated"

Java exposes six `Thread.State` values:

- **NEW:** created but not started;
- **RUNNABLE:** executing in the JVM or eligible to execute;
- **BLOCKED:** waiting to acquire a monitor lock;
- **WAITING:** waiting indefinitely for another action;
- **TIMED_WAITING:** waiting for up to a specified duration;
- **TERMINATED:** execution has ended.

These are JVM states, not a one-to-one representation of operating-system thread
states.

~{Java thread lifecycle states}(<java-thread-states.json> "The six Thread.State values and representative transitions between RUNNABLE and waiting states.")

### How does a thread enter the non-runnable state

!!! info "AI-generated"

- Contending for a `synchronized` monitor produces `BLOCKED`.
- `Object.wait()` and an untimed `Thread.join()` produce `WAITING`.
- `Thread.sleep`, timed `wait`, and timed `join` produce `TIMED_WAITING`.
- `Object.wait()` releases the monitor on which it waits; `Thread.sleep()` does
  not release monitors already held.
- `thread.join()` waits for `thread` to terminate; it pauses the caller, not the
  target thread.

---

## Thread Safety

A code that is safe to call by multiple threads simultaneously is called thread-safe.

### Critical Area

A critical area is a __section of code that is executed by multiple threads and where the sequence of execution for the threads makes a difference in the result__ of the concurrent execution of the critical area.

The critical area could appear only when __one or more threads write to the shared resources__. It is safe to let multiple threads read the same resources, as long as the resources do not change.

### Race Conditions

A race condition is a special condition that may occur inside a critical area.

When the result of multiple threads executing a critical area may differ depending on the sequence in which the threads execute, the critical area is said to contain a race condition.

### Which resources are Thread-Safe

!!! info "AI-generated"

~{Thread stacks and shared heap objects}(<java-memory-sharing.json> "Each thread has a private stack, while local references may point to the same mutable heap object.")

## Multithreading in Practice

### Running computation into a separate thread - spawning threads

Using Thread class:

```java
class MyClass extends Thread {
    @Override
    public void run() {
        //...
    }
}
```

Using Runnable interface:

```java
new Thread(new Runnable() {
 @Override
 public void run() {
  //…
 }
});
```

### Basic Thread synchronization

Thread might "cache" some shared data and prevent scanning it when other threads modify it.
> Use `volatile` keyword in the data field declaration to avoid this.

`t1.join()` returns only when `t1` finishes; it blocks whichever thread called
`join`, which is not necessarily the main thread.

To fixing thread interleaving (on a modifiable data):

- Make the modification operation "atomic" by making methods for each operation *synchronized* using `public synchronized void fn()`.
- Java `Object` implements and intrinsic lock (mutex) if we use `synchronized` keyword, a thread can only access the object if the lock is available.

Problem with synchronized methods:

- `total time taken = (no. of threads) * (unit work time)` => multithreading advantage is compromised.
- Independent methods still have to be executed sequentially (as the lock on object is no available while some thread accessing some orthogonal/independent method).

__Solution:__

__synchronized block__ with different locks for each independent code block (use n - different objects to act as locks and pass them to synchronized of each block)
> Default it is `synchronized(this)`
> Bad practice to lock on actual working object (shared data), multiple of them might point to the same (java optimization).
> Better to create separate locks.

### Thread Pools

Way of managing lots of threads at the same time.
> a collection of fixed number of workers

```java
//no. of workers
int n = 10;
//defining thread pool with fixed size
ExecutorService executor = Executors.newFixedThreadPool(n)

//allotting tasks to the executor service
executor.submit(new myCustomThread1());
executor.submit(new myCustomThread2());
//...

//stop accepting new tasks and it will shutdown after all are completed.
executor.shutdown();

//waits only for specified time and then will return
executor.awaitTermination(100, TimeUnit.MILLISECONDS);
```

Implementing thread-pool from scratch

- [jenkov](http://tutorials.jenkov.com/java-concurrency/thread-pools.html)
- [javacodegeeeks](https://www.javacodegeeks.com/2016/12/implement-thread-pool-java.html)
- [caffinc - simple-threadpool](https://caffinc.github.io/2016/03/simple-threadpool/)

### CountDownLatch

A thread safe class

```java
//initialize with a count
CountDownLatch latch = new CountDownLatch(10);
//counting it down
latch.countDown();
//wait till it is 0
latch.await();
```

### Concurrent (thread-safe) Data structures

!!! info "AI-generated"

`java.util.concurrent` provides concurrent collections, queues, synchronizers,
executors, and atomic utilities. Their individual operations have documented
thread-safety guarantees, but a multi-step check-then-act sequence may still need
an atomic method such as `compute`, an explicit lock, or another coordination
mechanism.

### BlockingQueue

```java
BlockingQueue<Integer> queue = new ArrayBlockingQueue<Integer>(size);

//patiently waits till queue-size < size
queue.put(someInt);

//patiently waits till an item is added (if queue is empty)
int val = queue.take();
```

> Both the above methods makes it easy to implement producer-consumer problem.

### Wait-Notify

#### Wait

- Can only be called inside the synchronized block
- Releases the lock on the object "immediately", it is synchronized on and waits for notification/resumption.

#### Notify

- Can only be called inside the synchronized block.
- Notifies the waiting thread. (does not release the lock until the block is over).

#### Notify-All

- Wakes all threads waiting on the same monitor. They still must reacquire that
  monitor after the notifying thread releases it.

### Re-Entrant Lock

```java
//lock interface
Lock lock = new ReentrantLock();
```

Bad way to use:

```java
//works just like synchronized block
lock.lock();
//do something -> if this throws and exception lock is never released!
lock.unlock();
```

Better way:

```java
lock.lock();

try {
    //do something
} catch (Exception e) {

} finally {
    lock.unlock();
}
```

Similar to wait/notify in the synchronized block:

```java
Condition condition = lock.newCondition();
//similar to wait()
condition.await();
//notify
condition.signal();
//notifyAll
condition.signalAll();
```

> We have to unlock before we can return to the waiting thread after calling signal()

### Deadlock

2 threads are waiting on each other to release a lock (free the shared resource) -> application frozen.

> Simple way to reproduce: lock the different re-entrant locks in different order in each thread.

Deadlock solutions:

- Lock your locks in the same order in every thread.
- Use `tryLock()` of the Lock interface.

```java
//it returns immediately the status (if success)
boolean gotLock = lock.tryLock()
//we should unlock the locks if partially acquired

//either we should have all the locks (acquired in order)

//or none (so that other can acquire them)
```

### Semaphores

```java
Semaphore sem = new Semaphore(noOfPermits);
//fair semaphore -> new Semaphore(permits, true);
//it will provide access to the first waiting thread on releasing.

//get current no. of available permits
sem.availablePermits();

//acquire -> decrements permits, waits if the permits == 0
sem.acquire();

//release -> increments permits.
sem.release();
```

- Semaphore with one permit = Lock
- Can be used to provide "limited-access" -> connection singleton managing connected users - max up to a limit (say 100).

### Callable and Future

To get return results in a scenario of multiple threads in a thread pool.

__Callable__ - Similar to Runnable but its thread method returns something (unlike Runnable's void run() method).

```java
// anonymous implementation to return integer
executor.submit(
    //anonymous class implementing Callable<T> interface
    new Callable<Integer>() {
        public Integer call() {
            //do something and return an int
        }
    }
);
```

__Future__ - Very useful for thread execution info/results

```java
//executor.submit(..) return a Future<T> instance
Future<Integer> future = executor.submit(…);

//get returned value
future.get();
//get() will block until the thread associated with the future has returned/executed.
```

#### Interrupts

```java
t1.interrupt();
//doesn't stop the thread -> there is a stop() method but it is deprecated.
//it just sets an interrupted flag and continues with the normal execution.

// Check the current thread without keeping another Thread reference.
Thread.currentThread().isInterrupted();

//catching InterruptedException will catch it if the flag is set.
```
