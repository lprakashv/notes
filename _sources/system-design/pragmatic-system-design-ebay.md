# Pragmatic System Design - eBay

## Questions

- How many simultaneous auctions we need to support? => __100K__ (items sold)
- How many bidder are there per auction? => 10-1000
- How many bids are there on average? => 5
- How long is an average auction? => 24 hours

## Basic Design

- Database with [ item_id, price ]
- POST API for placing bid with [ item_id, price ]
- Bid Service checks current top bid and updates the database if success else returns with an outbid message
  - Suffers concurrency issues -> race condition

## Optimistic Locking of Bids

- Failing bids fails right away (just like before)
- Successful bid updates the DB with "idempotent condition" which makes sure it didn't change from the last checked price.
  - Still suffers the race condition when updated price is still lesser than the requested bid

## Serialization / Sequential

- Bid Service no longer talks directly do DB
- It puts the bid into a queue
- Another "serializer" service polls the queue and checks the DB then updates it if necessary

## Even-Driven (Notifying to client)

- Another queue for the response (accepted/rejected) can be used from serializer to bid service for notifying the client.
- Using HTTP/REST, the client will be waiting
  - Web sockets can be used
  - On reconnection of the client, we can check either
    - Check the DB
    - Replay all the messages from the queue => event-sourcing

## Scaling

- Writes
  - 5 bids per user, 1000 peak users, 100K items => __8K per sec__
- Reads (response queue)
  - Every bid will require a read from the DB => __8K selects per sec__
  - Every bid will produce a message in the queue => __8K messages per sec__
- Number are fairly manageable using single large instance of a DB and single queue
- Reads can be scaled using read-replicas
- Writes can be scaled using sharding

![Final Design](./images/psd-ebay.png)
