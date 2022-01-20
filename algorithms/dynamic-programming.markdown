# Dynamic Programming Patterns

DP problem often has following characteristics:

- __Optimal Substructure__ - Optimal solution to the problem can be achieved from solving optimal solution for sub-problems
- __Overlapping Sub-problems__ - Sub problems are overlapping in nature
  - Greedy problems also have "optimal substructure" but the sub-problems are "not overlapping"

2 Approaches:

__Bottom-Up (Tabulation)__

```txt
// Pseudo-code example for bottom-up

F = array of length (n + 1)
F[0] = 0                       // base-case-1 (example - fibonacci)
F[1] = 1                       // base-case-2 (example - fibonacci)
for i from 2 to n:
    F[i] = F[i - 1] + F[i - 2] // sub-solutions (example - fibonacci)
```

__Top-Down (Memoization)__

```txt
// Pseudo-code example for top-down

memo = hashmap
Function F(integer i):
    if i is 0 or 1:                   // base-case (example - fibonacci)
        return i
    if i doesn't exist in memo:
        memo[i] = F(i - 1) + F(i - 2) // sub-solutions (example - fibonacci)
    return memo[i]
```

__2 Characteristics to Identify if problem is DP?__

First - The problem will ask for the optimum value (maximum or minimum) of something, or the number of ways there are to do something. For example:

- What is the minimum cost of doing...
- What is the maximum profit from...
- How many ways are there to do...
- What is the longest possible...
- Is it possible to reach a certain point...

> Note: Not all DP problems follow this format, and not all problems that follow these formats should be solved using DP. However, these formats are very common for DP problems and are generally a hint that you should consider using dynamic programming.

Second - Future "decisions" depend on earlier decisions. Deciding to do something at one step may affect the ability to do something in a later step. This characteristic is what makes a greedy algorithm invalid for a DP problem - we need to factor in results from previous decisions.

NOTE:

- Divide and conquer approaches can be parallelized while dynamic programming approaches cannot be (easily) parallelized
  - The subproblems in divide an conquer approaches are independent of one another (they do not overlap) while in dynamic programming, the subproblems do overlap

## Knapsack

- Given a set of items with 'w' weight and 'v' value.
- Items to include with a total weight 'M' in mind.
- Resource allocations with financial constraints.

2 Types:

### Divisible Knapsack

If we can take fraction of items.

- Greedy algorithm will provide optimal result.
  - Sort the items according to their value [ O(N logN) ]
  - Start with the item with max value and take as much as possible, then try with the next item in the sorted list [ O(N) ]
  - Total complexity = __N*logN + N = O(N)__

### 0-1 Knapsack

- Greedy algorithm will not provide optimal result!
- DP Approach:
  - Dp matrix for solutions:
    - `s[i][w]` => solution to first 'i' items and 'w' weight.
    - Describes maximum cost of the items that fits inside knapsack of size 'w' choosing from the first 'i' items.
  - We have to decide "whether to take the item of not".
  - `s[I][w] = max( s[ i-1 ][ w ]  ,   v[ I ] + s[ i-1 ][ w-w[i] ] )`

Cannot take fractions, we have to decide whether to take the item (1) or not (0).

## Min/Max cost/path/sum to Reach a Target

__Approach:__

1. Choose minimum (maximum) path among all possible paths before the current state, then add value for the current state.
2. `routes[i] = min(routes[i-1], routes[i-2], ... , routes[i-k]) + cost[i]`.

```java
for (int i = 1; i <= target; ++i) {
   for (int j = 0; j < ways.size(); ++j) {
       if (ways[j] <= i) {
           dp[i] = min(dp[i], dp[i - ways[j]] + cost / path / sum) ;
       }
   }
}

return dp[target]
```

__Example problems:__

- Min cost of climbing stairs
- Min path sum
- Coin change problem

## Distinct ways - no of all possible ways to rech the target

__Approach:__

1. "Sum" of all possible ways to reach the current state (i).
2. `routes[i] = routes[i-1] + routes[i-2], ... , + routes[i-k]`

```java
for (int i = 1; i <= target; ++i) {
   for (int j = 0; j < ways.size(); ++j) {
       if (ways[j] <= i) {
           dp[i] += dp[i - ways[j]];
       }
   }
}

return dp[target]
```

__Example problems:__

- Climbing stairs
- Unique paths
- no. of dice rolls with target sum.
- Knight probability in chessboard
- Partition equal subset sum.

## Merging intervals

__Approach:__

Find all optimal solutions for every
interval and return the best possible answer.

__Code approach:__

1. From i to j
2. `dp[i][j] = dp[i][k] + result[k] + dp[k+1][j]`

Get the best from the left and right sides and add a solution for the current position.

```java
for(int l = 1; l<n; l++) {
   for(int i = 0; i<n-l; i++) {
       int j = i+l;
       for(int k = i; k<j; k++) {
           dp[i][j] = max(dp[i][j], dp[i][k] + result[k] + dp[k+1][j]);
       }
   }
}

return dp[0][n-1]
```

__Example problems:__

- Min cost tree from leaf value
- Unique binary search trees.
- Min cost to merge stones

## DP on Strings

Given 2 strings where lengths are not too big

### 2 strings

```java
// i - indexing string s1
// j - indexing string s2

for (int i = 1; i <= n; ++i) {
   for (int j = 1; j <= m; ++j) {
       if (s1[i-1] == s2[j-1]) {
           dp[i][j] = /*code*/;
       } else {
           dp[i][j] = /*code*/;
       }
   }
}
```

### 1 string

```java
for (int l = 1; l < n; ++l) {
   for (int i = 0; i < n-l; ++i) {
       int j = i + l;
       if (s[i] == s[j]) {
           dp[i][j] = /*code*/;
       } else {
           dp[i][j] = /*code*/;
       }
   }
}
```

__Example problems:__

- Longest common subsequence (LCS)
- Palindromic substrings
- Longest palindromic subsequence
- Min ascii delete sum of 2 strings

## Decision making

Given a set of values find an answer with an option to choose or ignore the current value

__Approach:__

If you decide to choose the current value use the previous result where the value was ignored; vice-versa, if you decide to ignore the current value use previous result where value was used.

```java
// i - indexing a set of values
// j - options to ignore j values

for (int i = 1; i < n; ++i) {
   for (int j = 1; j <= k; ++j) {
       dp[i][j] = max({dp[i][j], dp[i-1][j] + arr[i], dp[i-1][j-1]});
       dp[i][j-1] = max({dp[i][j-1], dp[i-1][j-1] + arr[i], arr[i]});
   }
}
```

__Example problems:__

- House robber
- Best time to buy and sell stocks
