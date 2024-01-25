# Java Snippets

## Array

```java
Arrays.fill(array, value);

/** Copy array: */
System.arraycopy(
 int[]    source_array,
 int      start,
 int[]    dest_array,
 int      start2,
 int      end
);
```

## Map

```java
map.getOrDefault(key, defaultVal);

map.putIfAbsent(key, value);

//smallest
treeMap.firstEntry();
// greatest key less than 'k'
treeMap.floorKey(int k);
// greatest entry with key less than 'k'
treeMap.floorEntry(int k);
```

## Set

```java
/** Similar to tree map => tree set: */
// smallest
treeSet.first();
// greatest element less than 'k'
treeSet.floor(int k);
// smallest element with key greater than 'k'
treeSet.ceiling(int k);
```

## Queue

```java
PriorityQueue minHeap = new PriorityQueue<>();
PriorityQueue maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
```

## Bitwise Tricks

Test kth bit:

```java
s & (1 << k)
```

Set kth bit:

```java
s |= (1 << k)
```

Turn off kth bit:

```java
s &= ~(1 << k)
```

Toggle kth bit:

```java
s ^= (1 << k)
```

Multiple by 2n:

```java
s << n
```

Divide by 2n:

```java
s >> n
```

Intersection:

```java
s & t
```

Union:

```java
s | t
```

Set Subtraction:

```java
s & ~t
```

Extract lowest set bit:

```java
s & (-s)
```

Extract lowest unset bit:

```java
~s & (s + 1)
```

Swap Values:

```java
x ^= y; y ^= x; x ^= y
```
