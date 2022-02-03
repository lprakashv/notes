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

## Disjoint Set / Union-Find data structure

- Data structure to address connectivity of components in a network
- Allows to quickly find if two nodes are connected

Building a Disjoint set:

1. Given all the edges
2. We do the "Union" operation:
   1. We choose one of the vertices' in edge as the head, and add the vertices to a set - `head = choose(vertex1, vertex2)`, `set = new Set(head, [vertex1, vertex2, ...])`
   2. We keep adding both the vertices for each edge to their corresponding sets or creating new ones - `set = Set.find(vertex1, vertex2)`, `set.add(...)`
   3. Each set is such that for every element in set we can check what is their head - `set.head()`, `headOf(vertex)`
3. Merging sets will re-elect the head - `set3 = merge(set1, set2)`, `set3.head = choose(set1.head(), set2.head())`

Checking if two vertices are connected:

`headOf(vertex1) == headOf(vertex2)`

### Implementation of a Disjoint Set

Two functions:

- union
- find

```java
// range of vertices 0 - N-1
int N;

// edges - [vertex1, vertex2]
int[][] edges = new int[][]{{0, 1}, {0, 3}, {5, 6}, ...};

// This will be called a disjoint set or parent set
// parent of vertex='n' = parent[n]
// For root vertex, parent[n] = n
int[] parent = new int[N];

// Initially are nodes are 'root' nodes
for (int i=0; i<N; i++) parent[i] = i;

// Building Disjoin-Set
for (int[] edge : edges) {
  // both do not belong to any set - both are root nodes
  if (parent[edge[0]] == edge[0] && parent[edge[1]] == edge[1]) {
    // take any and make the other as its parent
    parent[edge[1]] = edge[0];
    continue;
  }

  // only one is independent - root node
  if (parent[edge[0]] == edge[0]) {
    // make the other as its parent
    parent[edge[0]] = edge[1];
    continue;
  }

  // TODO - similar for the other node as above

  // else case - both are part of a set!
  // find out root of vertex2
  int root2 = getRootNode(parent, edge[1]);
  // make one node as parent of other's
  parent[root2] = edge[0];
}

private int getRootNode(int[] parent, int node) {
  int root = node;
  while (root != parent[root]) {
    root = parent[root];
  }
  return root;
}

// find
public boolean checkConnectivity(int[] parent, int node1, int node2) {
  return getRootNode(parent, node1) == getRootNode(parent, node2);
}
```

### Quick Find

```java
// UnionFind.class
class UnionFind {
  private int[] root;

  public UnionFind(int size) {
    root = new int[size];
    for (int i = 0; i < size; i++) {
      root[i] = i;
    }
  }

  // O(1)
  public int find(int x) {
    return root[x];
  }
  // O(N)
  public void union(int x, int y) {
      int rootX = find(x);
      int rootY = find(y);
      if (rootX != rootY) {
        for (int i = 0; i < root.length; i++) {
          if (root[i] == rootY) {
            root[i] = rootX;
          }
        }
      }
  }
  // O(1)
  public boolean connected(int x, int y) {
    return find(x) == find(y);
  }
}
```

### Quick Union

```java
class UnionFind {
  private int[] root;

  // O(N)
  public UnionFind(int size) {
    root = new int[size];
    for (int i = 0; i < size; i++) {
      root[i] = i;
    }
  }

  // O(N)
  public int find(int x) {
    while (x != root[x]) {
      x = root[x];
    }
    return x;
  }

  // O(N)
  public void union(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY) {
      root[rootY] = rootX;
    }
  }

  // O(N)
  public boolean connected(int x, int y) {
    return find(x) == find(y);
  }
}
```

Quick-Union is more efficient than Quick-Find

- Time-complexity of `find` in quick-find = `O(1)`, while worst-case time-complexity of `find` in quick-union = `O(N)`, when graph is made like a linked-list. It's not always the case
- Time-complexity of `union` in quick-find = `O(N)`, while time-complexity of `union` in quick-union depends upon `find`. Since, average-case time-complexity of `find` `< O(N)`, average-case time-complexity of `union` `< N * O(N) < O(N^2)`

### Union by Rank - Quick-Rank (optimization to `union` method for Quick-Union)

- To join two nodes of independent graphs, choose a root-node such that resultant graph has lower height/depth.
- It is an optimization for union-based DSs - quick union sets.

```java
class UnionFind {
  private int[] root;
  private int[] rank;

  // O(N)
  public UnionFind(int size) {
    root = new int[size];
    rank = new int[size];
    for (int i = 0; i < size; i++) {
      root[i] = i;
      rank[i] = 1;
    }
  }

  // O(log N)
  public int find(int x) {
    while (x != root[x]) {
      x = root[x];
    }
    return x;
  }

  // O(log N)
  public void union(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY) {
      if (rank[rootX] > rank[rootY]) {
        root[rootY] = rootX;
      } else if (rank[rootX] < rank[rootY]) {
        root[rootX] = rootY;
      } else {
        root[rootY] = rootX;
        rank[rootX] += 1;
      }
    }
  }

  // O(log N)
  public boolean connected(int x, int y) {
    return find(x) == find(y);
  }
}
```

### Path compression (optimization to `find` method for Quick-Union)

- Quick-Find's `find` method is already optimized.

```java
class UnionFind {
  private int[] root;

  // O(N)
  public UnionFind(int size) {
    root = new int[size];
    for (int i = 0; i < size; i++) {
      root[i] = i;
    }
  }

  // O(log N)
  public int find(int x) {
    if (x == root[x]) {
      return x;
    }
    return root[x] = find(root[x]);
  }

  // O(log N)
  public void union(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY) {
      root[rootY] = rootX;
    }
  }

  // O(log N)
  public boolean connected(int x, int y) {
    return find(x) == find(y);
  }
}
```

### Final Optimized Union-Find (with Union-by-Rank and Path-compression)

```java
class UnionFind {
  private int[] root;
  // Use a rank array to record the height of each vertex, i.e., the "rank" of each vertex.
  private int[] rank;

  // O(N)
  public UnionFind(int size) {
    root = new int[size];
    rank = new int[size];
    for (int i = 0; i < size; i++) {
      root[i] = i;
      rank[i] = 1; // The initial "rank" of each vertex is 1, because each of them is
                    // a standalone vertex with no connection to other vertices.
    }
  }

  // O(α(N))
  // The find function here is the same as that in the disjoint set with path compression.
  public int find(int x) {
    if (x == root[x]) {
      return x;
    }
    return root[x] = find(root[x]);
  }

  // O(α(N))
  // The union function with union by rank
  public void union(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY) {
      if (rank[rootX] > rank[rootY]) {
        root[rootY] = rootX;
      } else if (rank[rootX] < rank[rootY]) {
        root[rootX] = rootY;
      } else {
        root[rootY] = rootX;
        rank[rootX] += 1;
      }
    }
  }

  // O(α(N))
  public boolean connected(int x, int y) {
    return find(x) == find(y);
  }
}
```

- Here `α` refers to the Inverse Ackermann function. In practice, we assume it's a constant. In other words, O(α(N)) is regarded as O(1) on average
