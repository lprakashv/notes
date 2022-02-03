# Designing Highly Available (HA) Database

## Questions

| Question | |
|-|-|
| Amount of data? | __100TB__ |
| Support updates? | Yes |
| Can the size of value so big, that doesn't fit in a single machine? | No, assume capped at 1GB |
| Estimated query per sec (QPS) | __100k__ |
| Latency | since it's HA, lower latency is preferred |
| C or A | A - as problems statement says |

## Estimations / Calculations

- Assuming a machine has 10TB hard-disk => 100TB / 10TB => __10 machines needed__
- Sharding will be required as 100TB can't be stored on a single machine
  - De-Normalized data would be easier to shard
  - If sharding criteria not chosen properly we can have inconsistency with storing normalized data (joins, keeping data unique)
    - Will be irrelevant in this as we are targeting eventual consistency

## Scaling

- We can have master-slave (read replicas) for each shard.
- 100k per sec (assuming all reads), assuming each machine can handle 10k reads per sec => 10 machines (read replicas) in worst case (all on single shard)
- Add-on: For Scaling writes we can have each machine store data and reconcile later!?

## HA Consideration

- Avoid single point of failure!
  - __Peer-to-Peer system__!
  - Similar to __Cassandra ring__!
- Replicated Consistent Hashing like Cassandra
- For faster writes (eventually consistent) `W = 1` `R = P` and for faster reads (in-consistent) `R = 1`, `W = P`
  - R - number of nodes to get quorum for read
  - W - number of nodes to be written to for writes to be successful
  - P - total nodes (replicated)
