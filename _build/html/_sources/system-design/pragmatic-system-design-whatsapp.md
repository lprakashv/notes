# Pragmatic System Design - WhatsApp

## Questions

- Active Users? => __100M users__
- Chats we need to support at a time? => __1M chats__
- Messages per day? => __1B / day__
- Platforms we need to support? => both mobile and web
- Do we need to support group chats? => No

## Basic design without scalability concerns

![Whatsapp basic](./images/psd-whatsapp-basic.png)

- Load balanced service with APIs:
  - __PUT /messages/{user_id}__
  - __GET /messages/{user_id}__
- A database: from_user, to_user, message, sent_at
- Calculations (identifying bottlenecks)
  - 1B messages per day => __12K messages per sec__ (inserts) - achievable with single node
  - 1M open chats, refreshing every 5 seconds (assumption) => __200K selects per second__ - "too much"!

## Scaling Reads

- Bottlenecks is polling every 5 seconds, leading to too many requests per second
- To make it push based system, we can use __"web sockets"__ => better but still won't solve the problem
- Read replicas can help
  - Assuming 10K read per node => __20 replicas__ of huge databases! We can do better!
- Sharding messages
  - Shard based on user as key => we have to query 2 shards for a [from, to] pair chats
  - Shard based on [from, to] pair, we will also end up querying 2 shards : [from, to] and [to, from]
  - Keeping __same Shard for [from, to] and [to, from]__ will fix out problem

Final Verdict: __Web Sockets__, chat database __Sharding__

## Scaling Chats (using queues)

- __20K reads per shard__ is still too much!
- We don't need to query database every time!
  - We just can query it for the first time a user connects to get the history!
- Queues can serve for all the real-time messages.
  - Websocket handler puts all the messages to the queue
  - Handler also subscribes to the queue and delivers the message
  - DB Writer also subscribes to the queue and writes the messages to the database shard using the shard-locator
  - __Impossible to have 1M queues__
    - We can use a __message multiplexer__ service which puts message in the one of the outbound queues after writing to database (limited 'N' maybe equals to number of websocket-handlers)

Final Verdict: __Limited N Queues__, __Message Multiplexer__

## Final Design

1. Client connects and fetches the history of conversation from a shard of database which sits behind the shard locator
2. Each message sent is sent to message-multiplexer
3. Message-multiplexer saves to the database and sends to the correct websocket-handler over a queue
4. Websocket-handler sends the message to the correct recipient over a websocket connection

![Whatsapp Final Design](./images/psd-whatsapp.png)

## Additional Notes

- Web-sockets (active connections) need to be used for realtime communication.
- Each machine has __65K ports available__, even if we use 1000 ports for internal or other communication, 60K ports can be used to maintain active connections
  - __1 machine can handle roughly 60K users__
- 2 kinds of messaging platforms:
  - Facebook : stores the messages permanently.
  - Whatsapp : deletes the messages once they are delivered!
- Cassandra
  - is not good for handling deletes well!
