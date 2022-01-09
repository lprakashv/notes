# Pragmatic System Design : Web Crawler

## Questions

- How many links? => Entire internet (__1.5B websites__)
- Where to start? => Start pages / reference will be provided
- When should we end? => Never
- Result? => Crawler should send all the pages to the indexer

## Basic Algo

1. Get URL
2. Fetch contents
3. Store
4. Extract URLs => Repeat for each

## Basic design

- Since, fetching from URLs which are "queued", we can intuitively use queues here!
- Queues
  - Poll URL from queue
  - Push extracted URLs into the queue
  - We can even use queue for pushing contents to the indexer and poll from it to extract the URLs

## Quirks / Optimizations - DNS

- Domain name resolution
- When dns is far away from our system each website crawled will reach to it and add additional latency
  - We can fix that but having our own DNS server

## Quirks / Optimizations - Javascript pages

- Modern SPA applications won't be rendered without JS and content is not accessible
- We can fix that by using "headless browser" in our content-fetcher service

## URLs

- We can use a part of the URL to know that it is the same page
- We need to have different frequency to crawl different type of pages
  - Sub-domains will get refreshed less frequently than the root domain
- Uniqueness
  - We can add a uniqueness-checker service
  - This can use "Bloom-filter" which is much more efficient than a hash-table / set.
    - We can use that in-memory of the URL-extractor component
    - 1.5B sites with each site having 10 pages (assumption) => __50GB RAM__
    - __Bloom-filter may five "false-positive"__ => 1 in a million miss => __15K pages never indexed__
    __- High throughput__, __low consistency__
  - We can use distributed K-V store like Redis
    - __700GB for 50 bytes each URL__
    - __70 shards with 10GB each__
    - __Medium throughput__, __medium consistency__
  - We can also use RDBMS
    - 700GB is not that much for RDBMS even with overhead 1TB is fine in a __single instance__
    - We can use read-replicas for uniqueness checking
    - __High consistency__, __low throughput__

## Priorities

- Requirements
  - We should be polite to the users
  - We should crawl different domains at different frequencies
- We can add Prioritizer service which makes decision to postpone and crawl (go/no-go decision)
- It can use Redis for last crawled domains
- It can use another queue for postponed tasks
- For frequency on each crawl we can check if it is changes from the last crawled => we increase the frequency if yes
- We can use updater service which is notified by indexer (owner of the content) => set the updated flag in the Redis

![Web Crawler Final Design](./images/psd-webcrawler.png)
