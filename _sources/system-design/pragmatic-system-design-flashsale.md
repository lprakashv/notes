# Pragmatic System Design - Flash coupon sale

## Questions

- How many users we have? => __100M active users__
- How many coupons we want to give away? => __10M__
- How long will it take us? => __10 min__

## Basic Design

Basic Algo:

1. Select coupon with user_id
2. Check if count(*) > 1M for the coupons table
3. Insert into coupons if not.

- Concurrency problems (as in bidding system / ebay)
- Scalability of our DB

## Quirks - Concurrency

- Cannot use locking as there is no row in coupons table yet!
- We cannot lock the entire table which can slow system down

Solutions:

- Solutions 1 : serialization using queue
  - 100M active users with 10 min to distribute coupons => 10M per min ~ 12M => __200K active users per sec__
  - 80M users per minute on peak => __1.2M users per sec__!
  - No single instance of service could handle that!
- Solution 2 : multiple queue consumers => will suffer from same problem of concurrency due to no single counter in-mem (classic check-then-act problem)
- Solution 3 : __pre-populate the coupons__ with 'null' user_id
  - We __only need 2 queries instead of 3__
  - Update coupons where user_id = null limit 1;
  - We can no-way create more coupons than we should!

## Scaling Reads

- If a server remembers which users have been given coupons we can avoid some reads
- How to make a user land on same server every time?
  - Level 7 LB by checking headers

## Scaling writes

- In memory cache of issues coupons
- In memory queue of coupons to issue => this can write at its own pace and reduce load on DB
- It is not "fair"
  - if one serve crashes and the same coupons will not be written and will be given to other users.
  - If one server exhausts all its coupons then no user will be able to get coupons if they land on that.
  - System is not "fair" and it need not be "fair" we just need to distribute 1M coupons.

![Final Design](./images/psd-flashsale.png)

Scaling using Queues

![Final Design 2](./images/psd-flashsale-queues.png)
