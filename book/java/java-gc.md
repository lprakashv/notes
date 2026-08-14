# Java Garbage Collection

## Heap

!!! info "AI-generated"

The Java heap stores ordinary objects and arrays managed by the garbage collector.
Most HotSpot collectors are generational:

- the **young generation** receives most new objects and is collected frequently;
- objects that survive enough collections may be promoted to the **old generation**.

Metaspace stores class metadata in native memory and is not a heap generation.
PermGen was removed in Java 8. Metaspace grows by default but can be capped with
`-XX:MaxMetaspaceSize`.

Thread stacks are private to their threads, but objects referenced from a stack
can still be shared. Thread safety depends on sharing and synchronization, not on
whether a reference happens to be held on a stack or in the heap.

~{HotSpot memory layout before and after Java 8}(<java-heap-layout.json> "PermGen was inside the pre-Java-8 heap; Metaspace uses native memory outside the heap.")

Key Heap features:

- If the JVM cannot allocate after collection, it may throw `OutOfMemoryError`.
- Access to the Heap is relatively slower in comparison to the Stack
- The collector reclaims objects that are no longer strongly reachable.
- Shared mutable objects need a concurrency strategy; immutable or thread-confined
  objects often do not need locking.

--

### Notes

Heap is divided into memory areas:

1. __NewGen__
    a. Eden space
    b. Surviving space 1
    c. Surviving space 2
2. __Old Gen__

This is a conceptual generational layout. Region-based collectors such as G1 use
non-contiguous regions rather than fixed contiguous young and old spaces.

Operations:

| Operation      | Description |
|----------------|-------------|
| Mark           | Starts from root of application, walks through "object graph", and marks all the reachable as live. |
| Sweep (delete) | Deletes all unreachable objects |
| Compacting     | Compacts the memory/defragment it/increase contiguous space. |

## Garbage Collector

A garbage collector is a JVM component that reclaims objects that are no longer
reachable.

> Different JVMs can have different algorithms of garbage collection, so there are a variety of different garbage collectors in Java.

Heap memory is divided into 2 sections called Generations: New generation and Old generation.

### Conceptual generational layout

!!! info "AI-generated"

~{Conceptual generational heap}(<java-generational-heap.json> "New objects enter Eden, survivors alternate between survivor spaces, and long-lived objects are promoted.")

New generation includes 3 regions: Eden, Survivor 0, and Survivor 1.

Old generation includes the Tenured region.

> So what happens when we create a new object in Java?

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

!!! info "AI-generated"

Current HotSpot provides these main collectors:

1. **Serial GC:** one GC thread; suitable for small heaps or constrained machines.
2. **Parallel GC:** stop-the-world collection using multiple threads, optimized
   primarily for throughput.
3. **G1:** generational, region-based, parallel, and mostly concurrent; the
   default on most supported hardware.
4. **ZGC:** generational and highly concurrent, designed for very short pauses at
   some throughput cost.

CMS was deprecated in JDK 9 and removed in JDK 14. Collector choice is a starting
point, not a guarantee: measure allocation rate, live-set size, throughput, and
pause distributions on the real workload.

---

## Garbage Collectors in Java

### G1 Garbage Collector

G1 was introduced in Java 7 and became the HotSpot default in Java 9 on most
supported configurations.

You can configure this for maximum pause time using flag `
-XX:MaxGCPauseMillis=n`.

> Lots of real-world studies say most of the objects (90%) garbage collected in a young generation or in first garbage collection or minor GC (also it depends upon applications). Who survived a couple of GCs(major GC), present in old memory (old objects) they will remain survive more than 95% times.

#### G1 Working

!!! info "AI-generated"

G1 divides the heap into equal-sized regions. At any moment a region may be free,
young, survivor, old, or humongous. Young collections evacuate live objects from
selected young regions. Concurrent marking estimates liveness in old regions;
later mixed collections evacuate selected young and old regions with useful
reclaim potential.

~{Contiguous spaces versus G1 regions}(<java-contiguous-vs-g1-regions.json> "A traditional contiguous layout is contrasted with dynamically assigned equal-sized G1 regions.")

G1 still has stop-the-world phases, including evacuation. It performs expensive
global marking mostly concurrently and reclaims space incrementally to pursue a
pause-time goal. A pause-time goal is a target, not a hard real-time guarantee.

#### G1 Extras

##### String deduplication

!!! info "AI-generated"

`String.intern()` returns a canonical pooled instance for equal strings. It changes
identity and lifetime behavior, so use it only when canonicalization is part of
the design—not as a blanket memory optimization.

G1 can instead deduplicate equal backing arrays for selected strings while keeping
the distinct `String` objects:

```bash
-XX:+UseG1GC -XX:+UseStringDeduplication
```

Inspect activity with `-Xlog:stringdedup*=debug`. The
`-XX:StringDeduplicationAgeThreshold` option controls when young strings become
eligible. Deduplication consumes CPU and bookkeeping memory, so measure retained
heap and throughput before enabling it in production.

### ZGC

!!! info "AI-generated"

ZGC is a scalable, highly concurrent collector for workloads where short pauses
matter more than maximum throughput. It was introduced as experimental in Java 11
and became a production feature in Java 15. Since JDK 24, only generational ZGC
remains.

```bash
java -XX:+UseZGC -Xms4g -Xmx4g -jar app.jar
```

ZGC performs marking, relocation, and reference processing mostly while
application threads continue to run. Load barriers and metadata associated with
object references let the collector relocate objects concurrently. The exact
reference layout and internal phases are implementation details that can change
between JDK releases; do not size or tune an application from a fixed bit diagram.

The current HotSpot guide describes sub-millisecond maximum pauses as the design
target and support from a few hundred megabytes to multi-terabyte heaps. Treat
those as collector goals, then validate latency and throughput with GC logs and a
representative load test.

Further reading: [HotSpot available collectors](https://docs.oracle.com/en/java/javase/25/gctuning/available-collectors.html).
