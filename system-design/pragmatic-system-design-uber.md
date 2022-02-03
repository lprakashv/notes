# Pragmatic System Design - Uber

Main Topics:

- Marketplace
- Geo-location
- Geo-sharding

## Marketplace type of system

- Usually 2 types of users
- demand / supply

## Riders

- __100M in total__ => affects the storage requirements
- __10M active__ => defines maximum requests per second (stresses the system the most)
- __10 rides per month__ on average

## Drivers

- __1M in total__
- __500K active drivers__
- Average shift : __6 hours__

NOTE : try to round the numbers (if random) up to help yourself

## Driver Locations

- Queues and gRPC are out of the way due to mobile app being the consumer of the system
  - We choose "web sockets", UDP would also have been fine as some message loss is tolerable due to it being a continuous message stream.
  - Payload : __driver_id, lat, long, direction__
- Calculations:
  - Drivers sending locations every 5 seconds (assumption)
  - 6 hour shifts => 4 shifts a day with 500K active drivers => __125K drivers at a time__
  - __25K location update requests per second__
  - Peak burst can be : 2X, 4K => __50K and 100K req per sec__

## Storing Locations

- Need to be able to support 50-100K writes per second
- Safely assuming each node can serve 5K writes per second
- We use sharing
  - Region / country based sharding => __Some shards become hotspots__
  - Custom polygon location shards (no overlap)
    - would need a __shard-locator service__
    - Lot of maintenance is required
      - Using __geo-spatial library__ mapping the entire globe into hexagons

## Getting Taxis Around Users

- Show max 10 drivers (assumption)
- Refresh every 5 seconds (keeping consistent with driver app)
- REST based, as we need 2 operations getting rides and placing order
- Calculations:
  - 5 app opens a day (assumption)
  - 1 minute average session (assumption) => __12 refreshes per session__
  - 10M active users => 50M app opens a day => 600M Requests per day => __7K req per sec__
- User can poll every 5 seconds the __"Driver Location service"__ based on user's general location
- __Shard-locator with read-replicas__ can be used (since these are read-only queries).
- For getting 10 closest drivers, use __geo-spatial query capability database (PostgresQL, MongoDB and MySQL-8 supports)__
  - If interviewer is not familiar with such databases,
    - We can use a __background worker to create a in-memory geo-spatial index__ ourselves using the driver-location database
    - Users will query the indexed in-memory data.

## User-Driver Matching

- Approaches
  - Sequential approach => give rider's offer to each driver one by one until someone accepts the offer
  - Parallel approach => give offer to all the drivers and first one to accept, wins the offer.
- We can introduce a __Drivers Gateway layer which has web-socket connections__ to all the drivers
- We can introduce a Rider Gateway layer where riders will request a match
- Matching service queries the driver-location database and calls the driver gateway for offer and notifies the rider
- Each internal services can talk to each other with gRPC

## Final Design

![Uber Final Design](./images/psd-uber.png)
