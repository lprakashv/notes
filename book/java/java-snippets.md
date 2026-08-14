# Java Snippets

## Array

!!! info "AI-generated"

```java
Arrays.fill(array, value);

System.arraycopy(
    sourceArray,
    sourceStart,
    destinationArray,
    destinationStart,
    length
);
```

## Map

!!! info "AI-generated"

```java
map.getOrDefault(key, defaultVal);

map.putIfAbsent(key, value);

//smallest
treeMap.firstEntry();
// greatest key less than or equal to k
treeMap.floorKey(k);
// greatest entry with key less than or equal to k
treeMap.floorEntry(k);
// greatest key strictly less than k
treeMap.lowerKey(k);
```

## Set

!!! info "AI-generated"

```java
// smallest
treeSet.first();
// greatest element less than or equal to k
treeSet.floor(k);
// smallest element greater than or equal to k
treeSet.ceiling(k);
// strictly less / strictly greater
treeSet.lower(k);
treeSet.higher(k);
```

## Queue

!!! info "AI-generated"

```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
```

## Bitwise Tricks

!!! info "AI-generated"

| Task | Expression |
|---|---|
| Test zero-based bit `k` | `(s & (1 << k)) != 0` |
| Set bit `k` | `s |= 1 << k` |
| Clear bit `k` | `s &= ~(1 << k)` |
| Toggle bit `k` | `s ^= 1 << k` |
| Intersection / union | `s & t` / `s \| t` |
| Set subtraction | `s & ~t` |
| Lowest set bit | `s & -s` |
| Lowest unset bit | `~s & (s + 1)` |
| Multiply by 2^n | `s << n` (subject to overflow) |
| Arithmetic right shift | `s >> n` |

For negative odd values, `>> n` rounds differently from integer division by 2^n.

Swap Values:

```java
int temporary = x;
x = y;
y = temporary;
```

The temporary-variable form is clearer and also works when both expressions refer
to the same storage location.

Reference: [Java Language Specification: bitwise and shift operators](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.22).
