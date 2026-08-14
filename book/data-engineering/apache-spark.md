# Apache Spark

## Introduction

Context

- Analysing large data sets
- Extending familiar functional abstractions over large clusters
- Distributed data parallelism in Spark

### Why Scala and Spark?

- If data becomes too large to fit into memory R/Python/Matlab won't allow you to scale! ( small data sets can be done very easily though ).
- Spark APIs directly maps to Scala collections (almost one-to-one)!
- Spark is more expressive (map, flatMap, filter etc.) than Hadoop's MapReduce.
- Performant in both running time and developer's productivity.
- Enables iterations (hard with Hadoop)

## Data-Parallel ( Distributed Data-Parallel )

### Shared memory data-parallel (multi-core)

- Split the data
- Workers/threads independently operate on data shards in parallel
- Combine when done (if necessary)

- Scala's parallel collections -> collection of abstraction over shared-memory data parallel execution.

### Distributed Data parallelism

- Split the data "over several nodes".
- Nodes independently operate on data shards in parallel.
- Combine when done (if necessary).
- We have to worry about "network latencies" between workers/nodes.
- [[ non-associative reduction can give non-deterministic/consistent/correct result in parallel execution ]]

__RDD:__ distributed counterpart of the Scala's parallel collection !

## Concerns (which Spark takes care for us):

- Partial failure
- Latency* -> cannot be masked completely

### Important latency figures

!!! info "AI-generated"

The exact numbers depend on hardware, storage, topology, and workload. The stable
lesson is the order of magnitude: local memory access is generally cheaper than
local storage, and both are cheaper and more predictable than a cross-network
shuffle. Measure the actual platform instead of designing from a fixed latency
table.

### What Spark's predecessor, MapReduce did to get so popular in 2000s

- Simple API -> map and reduce operations
- Fault tolerance  = Ability to recover for node failures -> any machine ( in that time )  was bound to fail, operate on data unthinkably without worrying about the node failures ! HUGE PLUS!

### Now, why Spark? If Hadoop's MapReduce works so well.

!!! info "AI-generated"

Classic MapReduce materializes intermediate results between jobs, which makes a
multi-stage or iterative workflow expensive. Spark builds a directed acyclic
graph of transformations and can cache reused datasets in memory.

Spark does **not** keep all data in memory. It can read from and spill to storage,
and wide transformations still shuffle data across the network. RDD lineage lets
Spark recompute lost partitions, while checkpointing can truncate very long or
expensive lineage. Performance gains depend on the workload, partitioning,
serialization, storage, and cluster—not on a universal “100×” multiplier.

## RDD

- Seem a lot like immutable sequential or parallel Scala collections.
- Many operations on RDDs are HOFs (taking f as args and returning RDD).

### Creating an RDD -> 2 ways

- Transforming an existing RDD.
- From a SparkContext ( or SparkSession ) object.
  - Parallelise -> convert a local Scala collection to an RDD.
  - textFile -> read a text file from HDFS or a local file system into an RDD[String]

### In Scala

- Transformers: Returns new collections as result ( map, flatMap, filter etc. )
- Accessors: Returns single values as result ( reduce, fold, aggregate, etc. )

### In Spark

- Transformations: Returns new RDDs as result
  - Are lazy!
- Actions: Compute a result based on an RDD, and either returned or saved to an external storage system (HDFS)
  - Are eager!
