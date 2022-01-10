# Pragmatic System Design : TinyURL

## Questions

- How many URLs will be added per month? => __500M__
- For how long the URLs should be kept? => __5 years__

__Total URLs__ = 500M x 12 x 5 = __30B__

## Basic Design

- Writes per sec
  - 500M per month => __300 per sec__
  - 10X peak load => __3K__
- Storage requirements
  - 30B URLs
  - Each URL takes 100 bytes (assumption) => __3TB__
- Load and storage is not much and can be easily fit into a single relational DB
- Identifier generator is needed

## Short Identifiers

- Requirements
  - As short as possible
  - Random
  - Human readable
- Base 58
- 6 characters are fine

## Scaling Reads

- __100:1 reads:writes__ ratio (assumption)
- 300 writes per sec => __30K reads per sec__
- At 10x peak => __300K reads per sec__!
- Assuming since instance can process 10K selects per sec => __6 replicas__
  - Can be costly considering 3TB of data with 6 instances
- Alternative : K-V storage like Redis
  - Single instance can process reads at 100K req per sec
  - Only 3 read replies are sufficient
  - Assuming 64GB RAM machines used and 3 replicas => __50 instances required__!
  - Again not as efficient!

Final Verdict: Lets keep the __RDBMS with 6 replicas__

## Adding Cache

- Using distributed cache can improve reads latency
- Calculations
  - 1% of 3TB => 30GB
  - 300K peak reads
  - 300K / 4 machines => __< 100K per sec__
- We can even improve the latency further while reading from remote cache by adding an __in-mem cache in each server__

![Final Design](./images/psd-tinyurl.png)
