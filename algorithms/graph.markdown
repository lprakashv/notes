# Graph Algorithms

```java
@Data
class Node<T> {
  T data;
  List<Node<T>> neighbors = new ArrayList<>();
}

@Data
class Graph<T> {
  List<Node<T>> nodes = new ArrayList<>();
}
```

## Topological Sort

- Given a DAG
- For every Edge U-V, U should always appear V
- Can be multiple topological-sort for a DAG

Applications:

- Build system with package dependency graph, deciding which package to build first.

Need:

1. Hash Set (visited) - To keep "visited" vertices
2. Stack (sorted) - Result. Vertices in topological sorted order OR List with reverse order.

Algo:

1. Visit each vertex in graph recursively
2. Keep pushing vertices in visited as we visit
3. Keep exploring only the non-visited vertices
4. Push the vertex in sorted stack

Algo Impl - Java:

```java
public List<T> topSort(Graph<T> graph) {
  List<T> res = new ArrayList<>();
  Set<Node<T>> visited = new HashSet<>();

  for (Node<T> node : graph.nodes) {
    topSortRecur(node, res, visited);
  }

  Collections.reverse(res);
  return res;
}


private void topSortRecur(Node<T> node, List<T> res, Set<Node<T>> visited) {
  visited.add(node);

  for (Node<T> n: node.neighbors) {
    topSortRecur(n, res, visited);
  }

  res.add(node);
}
```

## Dijkstra's Algo

- Single source shortest path algo.

Given: A Graph and a source node.
Result: Shorted path to all the other vertices of the graph from source.

NOTEs:

- Works on both directed and a-directed
- __Weights should be non-negative__
- __Greedy algo__
- Similar to Prim's algo for Minimum spanning tree
- Uses Heap and HashTable (PriorityQueue and HashMap)

Complexity: __E x log( V )__

- E = total number of edges
- V = total vertices

Initialization Needs:

1. vParent - Map of each vertex to its parent
2. vDistance - Map of each vertex to its distance from source
3. binaryMinHeap

Algo:

1. Initialize
   1. Add all the vertices to minHeap with INF as initial value
   2. Set the sourceVertex's value to 0 in minHeap
   3. Put source vertex in distance map with 0 value
   4. Put parent of source as null in parent map
2. While heap is not empty:
   1. Extract min node from heap and set to "current". (Will be source initially)
   2. Put current's weight into distance map
   3. For all the edges (child vertices) of the current node
      1. If the child vertex is "not in minHeap" -> "skip"
      2. Calculate newDistance = current's distance + edge's weight
      3. If minHeap's value for child vertex is higher than newDistance
         1. minHeap set child vertex's weight as newDistance
         2. Set child vertex's parent as current node

Algo Impl - Java: TODO

```java
@Data
class WeightedNode extends Node {
  Map<Node<T>, Integer>> neighborsWithDistances = new HashMap<>();
}

public void calculateShortedPathFrom(Graph<T> graph, WeightedNode<T> source) {
  // TODO
}
```

## Floyd Warshall's Algo

All pair shortest distance

- DP
- Works on directed and a-directed graphs
- Works even with negative weights

Applications:

- Clean's Algo
- Widest path
- Transitive closures

Variables and Data structures required: 2 NxN matrices, N = number of vertices

- path
- distance

Algo:

1. Initialize:
   1. Set distance/weight of all the edges in `"distance" matrix -> (I, j) = weight(I to j)`.
   2. Set all the non-direct paths we put INF in distance matrix.
   3. Set a unique value for every direct path in "path" matrix. (Usually the source to each the vertex).
2. "3" nested for-loops, `k: 0->N`, `i: 0->N`, `j: 0->N`:
   1. If `d[I][j] > d[I][k] + d[k][j]`  =>   `d[I][j] = d[I][k] + d[k][j]`
   2. `path[I][j] = path[k][j]`

The loop actually means:

- If going through a vertex "k", do we get a shorter distance from "i" to "j" via "k"?

Algo Impl - Java: TODO

```java
```
