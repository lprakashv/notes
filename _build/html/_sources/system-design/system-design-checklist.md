# System Design Checklist

## User Interface

- [ ] How are the users interacting with the system? - mobile, tablet, website, TV etc.

## LB

- [ ] Single node is being overloaded?
- [ ] Can be anywhere in the system, for proper resource utilization and reducing latency.

## Web Sockets Handler/Manager

Server keeping open websocket connections with all active user devices

- [ ] Central repository to keep track of which user is connected to which handler - Service called __WebSocket Manager__
- [ ] Graceful connection and disconnection of devices

## Storage Solution

- [ ] Images or Files? - S3
- [ ] Payment records (critical transactional data) - ACID compliant DB - Any RDBMS
- [ ] Multiple features, product related information (fluid unstructured data) - Document DB - Mongo
- [ ] Very low latency data - Cache - Redis

## CDN

- [ ] Geographically distributed data (closer to user who need it)

## Analytics Components

- [ ] There is always scope for analytics in any system! - usually never called out in any system design interview.
- [ ] Event Stream processing like Kafka-Streams, Spark-Streams - any even data is useful and can be used
- [ ] ML or scheduled processing? - Dump data in Hadoop and process later

## Pluggable Components

- [ ] Every large system will require multiple small components (or systems) - Twitter will need url-shortener, notification-system etc.

## Monitoring and Altering

- [ ] Everything needs to be monitored and alerts should be setup or for any critical resource limits, failure, threshold etc.

## Handling Special Edge Cases*
