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

- Reading from RAM/main mem. Is ~100x faster than reading from disk!
  - Read 1 MB from memory (main/RAM) -> 250us
  - Read 1 MB from disk -> 20ms ( 20000us )
- Main memory reference is ~1000000 ( 1M ) times faster than x-fer over the n/w US-Eu-US
  - Main mem. Ref -> 100ns
  - Send packet US-Eu-US -> 150ms ( 150000000ns )

### What Spark's predecessor, MapReduce did to get so popular in 2000s

- Simple API -> map and reduce operations
- Fault tolerance  = Ability to recover for node failures -> any machine ( in that time )  was bound to fail, operate on data unthinkably without worrying about the node failures ! HUGE PLUS!

### Now, why Spark? If Hadoop's MapReduce works so well.

- Hadoop/MapReduce
  - Fault tolerance in Hadoop/MapReduce comes at a cost!
    - B/w each map and reduce stage it shuffles the data and stores intermediate data in disk ( to recover for potential failures )
  - => Lot of n/w and disk!
- Spark
  - Retains fault tolerance but…
  - Uses FP -> keeps all data “in memory” and “immutable”.
  - All operations are functional-transformation (like regular Scala collections)
  - To achieve tolerance -> replaying functional-transformation on original dataset over and over again (without worrying about side-effects).
  - => 100x performance improvement over Hadoop!!!
  - => Even more expressive APIs than Hadoop!!!

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
