# Java Multi-threading

---

## Java `Thread` class methods

### `Thread.currentThread()`

The return type of this method is Thread, it returns a reference of currently executing thread (who touched this method). It does not raise any exception.

### `long getId()`

The thread ID is a positive long number generated when this thread was created.

The thread ID is unique and remains unchanged during its lifetime. When a thread is terminated, this thread ID may be reused.

### `int getPriority()` and `void setPriority()`

The priority of thread can either be assigned by the JVM or by the programmer explicitly while creating the thread.

The thread's priority is in the range of 1 to 10. The __default priority of a thread is 5__.

### `Thread.State getState()`

### `void interrupt()`

An interrupt is an indication to a thread that it should stop what it is doing and do something else. It’s up to the programmer to decide exactly how a thread responds to an interrupt, but __it is very common for the thread to terminate__.

### `void join()`

This java thread join method puts the current thread on wait until the thread on which it’s called is dead. If the thread is interrupted, it throws `InterruptedException`.

If the referenced thread was __already terminated__ or __hasn’t been started__, the call to `join()` method returns __immediately__.

### `void run()`

The `run()` method of a thread encapsulates the logic that should be run by a thread.

### `void setDaemon(boolean on)`

On the other hand, daemon threads are __low-priority threads whose only role is to provide services to user threads__. Since daemon threads are meant to serve user threads and are only needed while user threads are running, they won’t prevent the JVM from exiting once all user threads have finished their execution.

The method `setDaemon()` can only be called after the Thread object has been created and the thread has not been started. An __attempt to call setDaemon() while a thread is running will throw an `IllegalThreadStateException`__.

### `Thread.sleep(long millis)`

`Thread.sleep()` the method can be used to pause the execution of the current thread for a specified time in milliseconds. The argument value for __milliseconds can't be negative__, else it throws `IllegalArgumentException`.

### `void start()`

When a program calls the `start()` method, a new thread is created, and then the `run()` method is executed.

We can't call the `start()` method twice otherwise it will throw an `IllegalStateException`.

### `Thread.yield()`

`yield()` basically means that the thread is not doing anything particularly important and if any other threads or processes need to be run, they should run. Otherwise, the current thread will continue to run.

Use of yield method:

- Whenever a thread calls `java.lang.Thread.yield()` method, it gives hint to the thread scheduler that it is ready to pause its execution. The thread scheduler is free to ignore this hint.
- If any thread executes yield method, __thread scheduler checks if there is any thread with same or high priority than this thread__. If the processor finds any thread with higher or same priority then it will move the current thread to Ready/Runnable state and give processor to other thread and if not — current thread will keep executing.

---

## Thread Lifecycle

According to Sun microsystems, there are 4 states in the java thread life cycle.

- __New__ — A thread is in the "New" state, when an object of the __thread class is instantiated but the “start” method is not invoked__.
- __Runnable__ — When the __"start" method has been invoked on the thread object__. In this state, the thread is either waiting for the scheduler to pick it up for execution or it's already running. Let us call the state __when the thread is already picked for execution, the “running” state__.
- __Non-Runnable(Blocked , Timed-Waiting)__ — When the thread is alive, i.e., the thread class object exists, but it cannot be picked by the scheduler for execution. __It is temporarily inactive__.
- __Terminated__ — When the thread completes execution of its “run” method. At this stage, the task of the thread is completed.

![Thread Lifecycle](./images/threadlifecycle.png)

### How does a thread enter the non-runnable state

- __Forced reason__
  - It is waiting for an I/O operation.
  - It is waiting on an object which is being held by another thread (Java associates "Monitor" to every object to enforce locking/synchronization).
  - Moved to sleep by scheduler based on the logic of resource sharing.
- __By choice__ - we can code inside "run" method or any method inside run which can deliberately give up CPU time.
  - __`sleep(long millis)`__ thread gives up CPU time but keeps the lock.
  - __`wait()`__ or __`wait(long timeout)`__ causes thread to give up CPU time as well as release any object lock. If used without timeout, it remains in non-runnable state endlessly unless we call `notfy()` or `notifyAll()` on  it.
  - __`yield()`__ - This method is like a notification to the scheduler, that the thread is ready to give up execution. The scheduler then decides, based on other live threads and their priorities, if it wants to move the calling thread to runnable and give the CPU time to other threads, or keep running the existing thread.
  - __`join()`__ is called to pause the execution of the program until the thread calling the join method is terminated.

---

## Thread Safey

A code that is safe to call by multiple threads simultaneously is called thread-safe.

### Critical Area

A critical area is a __section of code that is executed by multiple threads and where the sequence of execution for the threads makes a difference in the result__ of the concurrent execution of the critical area.

The critical area could appear only when __one or more threads write to the shared resources__. It is safe to let multiple threads read the same resources, as long as the resources do not change.

### Race Conditions

A race condition is a special condition that may occur inside a critical area.

When the result of multiple threads executing a critical area may differ depending on the sequence in which the threads execute, the critical area is said to contain a race condition.

### Which resources are Thread-Safe

![Threadsafe](./images/threadsafe.jpeg)
