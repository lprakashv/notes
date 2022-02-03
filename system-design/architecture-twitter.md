# Twitter Architecture

## Scope of current architecture

- Tweet
- Timeline
  - Home
  - User
  - Search
- Trends

## Current Numbers

- 300M+ Users
- Writes - 600 tweets / sec
- Reads - 600,000 tweets / sec ~ __Read-heavy__

Additional Notes:

- Slight delay is fine ~ __Eventually consistent__

## Database

Tables

- Users
- Followers
- Tweets and ReTweets

Redis

- User-Followers List
- User-Tweets List
- Tweets? (cached)

## Home TimeLine

### Basic algo (first approach)

1. Get Source Users from Followers table for the user
2. Get their latest tweets
3. Merge their tweets and show sorted by timestamp

Why Wrong?

- Very ready heavy, DB reads won't scale

### Fan-out Apprach

Every User Tweet will

1. Put a `LPUSH` cache entry in it's own User-Timeline/Tweets
2. __Fan-out__ an `LPUSH` cache entry in __all the follower's__ __Home-Timeline__

Problem: Celebrity (100k-millions followers) will cause heavy load on cache writes

Solution: Keep a Celebrity-Follow entry as well for each user in Redis, merge before home-timeline generation

### Optimization

- We can save extra computation and memory in Redis by ignoring pre-computation for inactive users
  - Skip populating U-T and H-T cache entries for those users

## Trends

Basic data:

- Volume of the tweets
- Time taken

Uses:

- Apache Storm / Heron

(Other stream processing solutions can also be used)

<img src="./images/tweet-trends-pipeline.png" alt="tweet-trends-pipeline" width="600px"/>

- Filter - removes unnecessary tags (manually updated)
- Parser - Parses Tweet and add missing tags from text
- Geo-Location - Finds location of the tweet

Each processing unit can be scaled based on the particular load.

## Search Timeline

- "Distributed" __Inverted Full-text index__
- Uses __Earlybird__ based on Lucene (in-house)
- Query is served using Scatter and Gather from all the data-centers (because it is distributed)

## Final Design

<img src="./images/twitter-final.png" alt="twitter-final" width="800px"/>

Additional features:

- Inactive users's timeline is built in __Social-Graph__ service by querying the database
- DB is MySQL and is abstracted away using __Gizzad__ (in-house) which provides automatic replication
- Push based updates are given by WebSocket handlers (__1M connections__) through __Firehose__ wih __22MB/sec__ (one of the largest real-time event based system)
