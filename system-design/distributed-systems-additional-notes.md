# Distributed System Notes

Collection of independent computers that appear to the users as a single computer.

3 significant characteristics:

1. Concurrency of components.
2. Lack of global lock.
3. Independent failure of components.

## Why does my computer with a lot of peripherals and system is a distributed system?

- All share a global clock! — the common bus.
- Single master systems are much better!

## Scaling strategies for Single master database

### Read replication

- Single master database which updates many "follower" instances as copies for independent reads.
- Problems:
  - "CONSISTENCY"
  - COMPLEXITY
  - only for READ-HEAVY

### Sharding

- Write traffic is shared.
- Problems
  - COMPLEXITY
  - LIMITED DATA MODEL (worse in case of too many keys to shard upon)
  - LIMITED ACCESS PATTERNS

### Consistent Hashing and Replication

- Ring of nodes carrying the range of hash values, each coming key's hash give the node where the data/value could be written to or read from.
- Replication to following 'n' nodes make the data more redundant.
- Problems:
  - CONSISTENCY => EVENTUAL CONSISTENT
  - For strong consistency:
    - R (need to agree) + W (successfully took a write) > N (no of replicas)
- When to use:
  - Scale
    - If not scale: => go to single database
  - Transactional data (business transactions) => data that changes a lot!
    - If not !transactional_data: => go to hadoop
  - Always on (availability)

## CAP Theorem

- __Consistency__ : I read only the most recently written value.
- __Availability__ : When I request, I will be answered.
- __Partition tolerance__ : System is able to work correctly after a partition is  joined back.

NOTEs:

- __P - is at the core of the distributed system, non-negotiable.__
- __We have to make a choice among "C" and "A" in a distributed system.__
- __We get both "C" and "A" in a "non"-distributed (single node) system.__

Constraints:

- __CP__ — Cannot answer until system is sure of the answer (all nodes in sync).
- __CA__ — Gives the current (last synced) version (may get wrong answer).

## ACID for Transaction (bundle of changes)

- __Atomic__ - binary!
- __Consistent__ - Non the one from CAP, after transaction db is not broken.
- __Isolated__ - one transaction can't see another until after the first one completes.
- __Durable__ - everything is persisted.

## Distributed Computation

- Usually Scatter/Gather
- Keep the computation closer to where the data is!
  - Easier to distribute code (computation than moving data around)
  - Data is huge while tons of lines of code barely cross 100MB

Examples:

- MapReduce
- Hadoop
- Spark
- Storm

### MapReduce

- On (K, V)
- Mapper - K -> V
- Shuffler - collects (K,V) with common keys
- Reducer

### Hadoop (few things combined)

- MapReduce API
- MapReduce job management
- Distributed file system (HDFS)
  - File and directories
  - Metadata managed by a replicated master
  - Files stored in large, immutable, replicated blocks.
- ecosystem

When to use:

- __Data volume is large__
- __Velocity is low__
- Latencies SLAs are not aggressive.
- Not Fast! __Batch-mode__, slow, only for huge volumes

### Spark

- Scatter/Gather (similar to MapReduce)
- More general RDD (instead of K-V)
- More general programming mode => transform/action (similar to Map/Reduce)
- Storage agnostic.
