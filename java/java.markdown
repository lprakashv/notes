# Java Knowledge

## Garbage Collectors

Heap is divided into memory areas:

1. __Permgen__/__metaspace__
2. __NewGen__
    a. Eden space
    b. Surviving space 1
    c. Surviving space 2
3. __Old Gen__

> Only (2) and (3) are considered for GC.

### Operations

| Operation      | Description |
|----------------|-------------|
| Mark           | Starts from root of application, walks through "object graph", and marks all the reachable as live. |
| Sweep (delete) | Deletes all unreachable objects |
| Compacting     | Compacts the memory/defragment it/increase contiguous space. |

### GC Cycles - Triggering

In 2 types of ways of GC triggered:

| Type/Cycle |    |
|------------|----|
| Minor      | Works on small amount of memory - mostly the newgen space, old is untouched |
| Major      | Works on the entire heap |

- Both the operations are "stop the world"
- Every new object creation happens in Eden space.
- On Eden space exhaustion, minor gc kicks in.
  - Marks all the objects in New/young gen.
  - Puts surviving from eden in either SS1 or SS2
  - Also transfers surviving in other SS also (avoids compacting overhead)
  - Sweeps
- If an object survives `-XX:MaxTenuringThreshold` number of gc cycles, it's promoted to older/tenured space.

### Types of GC

1. Serial GC - basic.
   1. Single threaded.
   2. Completely pauses every other thread (complete stop the world).
2. Concurrent Mark Sweep (CMS).
   1. When: __more memory, more CPU, short pauses.__
   2. Performs GC along with application execution.
   3. Does not wait for the Old Gen to be full.
   4. Stops the world only during marking/re-marking.
3. Parallel GC.
   1. When: __less memory, less CPU, high throughput needed, can withstand long pauses.__
   2. Utilizes multiple CPUs and threads.
   3. Does not kick in until heap is full/near-full.
   4. "Stop the world".
4. G1 GC (Java 7+) - Garbase First.
   1. Divides entire memory into smaller regions (those can be Eden/Survivor/Tenured).
   2. Runs on smaller regions whichever has more garbage.
   3. Concurrent as well as parallel.
   4. Pauses for defragmentation.
   5. Better heap utilization.

## Java Multithreading

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

`t1.join()` returns to main thread only when `t1` finishes meaning `t1` __blocks__ the main thread.

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
Executor.awaitTermination(100, TimeOut.MILLIS);
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

- All classes in `java.util.cocurrent.*` package are concurrent and thread-safe.
- No need to worry about thread synchronization at all.

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

__Wait__

- Can only be called inside the synchronized block
- Releases the lock on the object "immediately", it is synchronized on and waits for notification/resumption.

__Notify__

- Can only be called inside the synchronized block.
- Notifies the waiting thread. (does not release the lock until the block is over).

__Notify-All__

- Notifies the waiting thread. (does not release the lock until the block is over).

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

### Interrupts

```java
t1.interrupt()
//doesn't stop the thread -> there is a stop() method but it is deprecated.
//it just sets an interrupted flag and continues with the normal execution.

//we cause Thread.currentThread() instead of explicitly defining a thread
t1.isInterrupted()

//catching InterruptedException will catch it if the flag is set.
```

## Strings

- String pool was used to be in Permgen, but __since java 8 it has been moved to main heap area__.
- Since java 1.7 `+` operators are implemented using `StringBuilder`'s `.append()` method.
- `.concat()` can only concat 2 strings (unlike `.append()` and `+` which can concat different data types)
- __There was a memory leak in java 1.6 `String()` constructor.__
- Regex - match introduced in java 8.

## Stream

- The data comes from elsewhere (a collection, array, generator function, or I/O channel) and is processed through a pipeline of computational steps to produce a result or side effect, at which point the stream is finished.
- Stream's __focus is on computation__, __not data__.
- Streams provide __no storage for the elements that they process__*, and the lifecycle of a stream is more like a point in time — the invocation of the terminal operation.
- For streams, __only the terminal operation is eager, all the others are lazy__.
- Stream operations represent a functional transformation on their input (also a stream), rather than a mutative operation on a data set (filtering a stream produces a new stream whose elements are a subset of the input stream but doesn't remove any elements from the source).

Example of non-stream vs stream operation:

```java
//Ad-hoc query over a collection

Set<Seller> sellers = new HashSet<>();
for (Txn t : txns) {
  if (t.getBuyer().getAge() >= 65)
    sellers.add(t.getSeller());
}

List<Seller> sorted = new ArrayList<>(sellers);

Collections.sort(sorted, new Comparator<Seller>() {
  public int compare(Seller a, Seller b) {
    return a.getName().compareTo(b.getName());
  }
});

for (Seller s : sorted)
  System.out.println(s.getName());
```

```java
txns.stream()
  .filter(t -> t.getBuyer().getAge() >= 65)
  .map(Txn::getSeller)
  .distinct()
  .sorted(comparing(Seller::getName))
  .map(Seller::getName)
  .forEach(System.out::println);
```

Key Advantages:

1. No distraction of garbage variable (sellers, sorted in the above example)
2. Don't have to keep track of context which leads to code understanding on one glance, less error prone.

## ClassLoader

__javac__ : `*.java` files to `*.class` files

__Class-loader__ : loads the `*.class` files!

Kinds of class loaders and load from locations:

1. __Bootstrap__ (or "Primordial ClassLoader")
    1. `JRE/lib/rt.jar`
2. __Extension__
    1. `JRE/lib/ext`
    2. Or any directory denoted by : `"java.ext.dirs"`
3. System or Application
    1. `"CLASSPATH"` environment variable.
    2. `"-classmate"` or "-cp" option.
    3. Classpath attribute of manifest inside JAR file.

### Bootstrap ClassLoader

- Loads standard JDK class files from "rt.jar"
- Parent of all class loaders
- Doesn't have any parent
  - `String.class.getClassLoader() == null`
- Only class loader which is __implemented in native language__, mostly in "C" !
  - __All others are implemented using `java.lang.ClassLoader`__

### Extension ClassLoader

- Delegates class loading request to its parent (Bootstrap)
- If unsuccessful from parent (Bootstrap), it loads class from `"jre/lib/ext"` or any directory pointed by `"java.ext.dirs"`
- Implemented by : `sun.misc.Launcher$ExtClassLoader`
- Child or Extension class loader

![ClassLoader](./images/jvm-classloader.png)

Principles:

1. Delegation principle: A class in loaded in Java when it is needed.
2. Visibility principle: Child ClassLoader can see class loaded by parent ClassLoader, but the vice-versa is not true.

Simple test to prove visibility principle

- Get Current class's ClassLoader by calling, `Abc.class.getClassLoader()` ====> Abc is an Application ClassLoader class
- If we try to load this class using the Extension class loader like:
  - `Class.forName("somepack.Abc", true, ClassLoaderTest.class.getClassLoader().getParent())`
  - This will fail! =====> meaning extension class loader cannot see the classes loaded by application class loader

Extras:

- Class is loaded by calling `loadClass()` method of `java.lang.ClassLoader` class which calls `findClass()` method to locate bytecodes for the corresponding class
- Extension ClassLoader uses `java.net.URLClassLoader` which searches for class files and resources in JAR and directories. any search path which is ended using "/" is considered a directory
- If `findClass()` does not found the class than it throws `java.lang.ClassNotFoundException` and if it finds it calls defineClass() to convert bytecodes into a `.class` instance which is returned to the caller
