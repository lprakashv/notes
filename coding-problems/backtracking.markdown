# Leetcode Notable Backtracking problems

## Combinations

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> list = new ArrayList<>();
    Arrays.sort(nums);
    backtrack(list, new ArrayList<>(), nums, 0);
    return list;
}

private void backtrack(List<List<Integer>> list , List<Integer> tempList, int [] nums, int start){
    list.add(new ArrayList<>(tempList));
    for(int i = start; i < nums.length; i++){
        tempList.add(nums[i]);
        backtrack(list, tempList, nums, i + 1);
        tempList.remove(tempList.size() - 1);
    }
}
```

## Permutations (without duplicates)

```java
public List<List<Integer>> permute(int[] nums) {
   List<List<Integer>> list = new ArrayList<>();
   // Arrays.sort(nums); // not necessary
   backtrack(list, new ArrayList<>(), nums);
   return list;
}

private void backtrack(List<List<Integer>> list, List<Integer> tempList, int [] nums){
   if(tempList.size() == nums.length){
      list.add(new ArrayList<>(tempList));
   } else{
      for(int i = 0; i < nums.length; i++){
         if(tempList.contains(nums[i])) continue; // element already exists, skip
         tempList.add(nums[i]);
         backtrack(list, tempList, nums);
         tempList.remove(tempList.size() - 1);
      }
   }
}
```

## Permutations with duplicates

```java
public List<List<Integer>> permuteUnique(int[] nums) {
    List<List<Integer>> list = new ArrayList<>();
    Arrays.sort(nums);
    backtrack(list, new ArrayList<>(), nums, new boolean[nums.length]);
    return list;
}

private void backtrack(List<List<Integer>> list, List<Integer> tempList, int [] nums, boolean [] used){
    if(tempList.size() == nums.length){
        list.add(new ArrayList<>(tempList));
    } else{
        for(int i = 0; i < nums.length; i++){
            if(used[i] || i > 0 && nums[i] == nums[i-1] && !used[i - 1]) continue;
            used[i] = true;
            tempList.add(nums[i]);
            backtrack(list, tempList, nums, used);
            used[i] = false;
            tempList.remove(tempList.size() - 1);
        }
    }
}
```

## Palindrome Partitioning

```java
public List<List<String>> partition(String s) {
   List<List<String>> list = new ArrayList<>();
   backtrack(list, new ArrayList<>(), s, 0);
   return list;
}

public void backtrack(List<List<String>> list, List<String> tempList, String s, int start){
   if(start == s.length())
      list.add(new ArrayList<>(tempList));
   else{
      for(int i = start; i < s.length(); i++){
         if(isPalindrome(s, start, i)){
            tempList.add(s.substring(start, i + 1));
            backtrack(list, tempList, s, i + 1);
            tempList.remove(tempList.size() - 1);
         }
      }
   }
}

public boolean isPalindrome(String s, int low, int high){
   while(low < high)
      if(s.charAt(low++) != s.charAt(high--)) return false;
   return true;
}
```

## N-Queens problem

placing 'N' chess queens on an N x N chessboard so that no two queens threaten each other

1. Iterate row-wise and try to place __1 queen on each row__
2. Place a queen on first position
   1. Place subsequent queen on the __first safe position__ in the subsequent row (i, j nested loop)
   2. If row remains empty:
      1. backtrack
      2. remove the previous queen
      3. place again

```java
int[][] table;
int numQueens;

void solve() {
  setQueens(0); // start with 0th column
  printTable();
}

boolean setQueens(int col) {
  // base case
  if ( col == numQueens ) return true;

  for ( int row = 0; row < numQueens; row++ ) {
    if ( isValid(row, col) ) {
      // assume/place queen
      table[row][col] = 1;

      // result found
      if ( setQueens( col+1 ) ) return true;

      // backtrack / reset
      table[row][col] = 0;
    }
  }
}
```

## max jumps from an array indices given, find if traversal possible or not

- Backtracking (2^n, n)
- DP (n^2, n)
- Greedy (n, 1)

[solution](https://leetcode.com/problems/jump-game/solution/)

## Phone number combinations

__Leetcode solution:__

```java
  Map<String, String> phone = new HashMap<String, String>() {{
    put("2", "abc");
    put("3", "def");
    put("4", "ghi");
    put("5", "jkl");
    put("6", "mno");
    put("7", "pqrs");
    put("8", "tuv");
    put("9", "wxyz");
  }};

  List<String> output = new ArrayList<String>();

  public void backtrack(String combination, String next_digits) {
    // if there is no more digits to check
    if (next_digits.length() == 0) {
      // the combination is done
      output.add(combination);
    }
    // if there are still digits to check
    else {
      // iterate over all letters which map
      // the next available digit
      String digit = next_digits.substring(0, 1);
      String letters = phone.get(digit);
      for (int i = 0; i < letters.length(); i++) {
        String letter = phone.get(digit).substring(i, i + 1);
        // append the current letter to the combination
        // and proceed to the next digits
        backtrack(combination + letter, next_digits.substring(1));
      }
    }
  }

  public List<String> letterCombinations(String digits) {
    if (digits.length() != 0)
      backtrack("", digits);
    return output;
  }
```

__My solution:__

```java
public List<String> letterCombinations(String digits) {
    if (digits == null || digits.length() == 0) return new ArrayList<>();

    Map<Character, List<Character>> map = new HashMap<>();

    map.put('2', Arrays.asList('a', 'b', 'c'));
    map.put('3', Arrays.asList('d', 'e', 'f'));
    map.put('4', Arrays.asList('g', 'h', 'i'));
    map.put('5', Arrays.asList('j', 'k', 'l'));
    map.put('6', Arrays.asList('m', 'n', 'o'));
    map.put('7', Arrays.asList('p', 'q', 'r', 's'));
    map.put('8', Arrays.asList('t', 'u', 'v'));
    map.put('9', Arrays.asList('w', 'x', 'y', 'z'));

    List<String> res = Arrays.asList("");

    for (char sc: digits.toCharArray()) {
        List<String> localList = new ArrayList<>();
        for (String s: res) {
            for (char c : map.get(sc)) {
                localList.add(s + c);
            }
        }
        res = localList;
    }

    return res;
}
```

## Generate parenthesis, given 'n'

```java
public List<String> generateParenthesis(int n) {
    List<String> ans = new ArrayList();
    if (n == 0) {
        ans.add("");
    } else {
        for (int c = 0; c < n; ++c)
            for (String left: generateParenthesis(c))
                for (String right: generateParenthesis(n-1-c))
                    ans.add("(" + left + ")" + right);
    }
    return ans;
}
```

## Permutations of an array

```java
  public void backtrack(int n,
                        ArrayList<Integer> nums,
                        List<List<Integer>> output,
                        int first) {
    // if all integers are used up
    if (first == n)
      output.add(new ArrayList<Integer>(nums));
    for (int i = first; i < n; i++) {
      // place i-th integer first
      // in the current permutation
      Collections.swap(nums, first, i);
      // use next integers to complete the permutations
      backtrack(n, nums, output, first + 1);
      // backtrack
      Collections.swap(nums, first, i);
    }
  }

  public List<List<Integer>> permute(int[] nums) {
    // init output list
    List<List<Integer>> output = new LinkedList();

    // convert nums into list since the output is a list of lists
    ArrayList<Integer> nums_lst = new ArrayList<Integer>();
    for (int num : nums)
      nums_lst.add(num);

    int n = nums.length;
    backtrack(n, nums_lst, output, 0);
    return output;
  }
```

## Word search in matrix (any snaky)

> backtracking / DFS with reset visited on mismatch

```java
private boolean util(char[][] board, boolean[][] visited, int i, int j, String word, int wi) {
    if (wi >= word.length()) return true;

    if (i < 0 || i >= board.length || j < 0 || j >= board[0].length
    || visited[i][j]
    || word.charAt(wi) != board[i][j]) return false;

    visited[i][j] = true;

    if (util(board, visited, i-1, j, word, wi+1)
        || util(board, visited, i, j-1, word, wi+1)
        || util(board, visited, i+1, j, word, wi+1)
        || util(board, visited, i, j+1, word, wi+1)) return true;

    visited[i][j] = false; // reset for backtracking
    return false;
}

public boolean exist(char[][] board, String word) {
    if (board == null || board.length == 0 || board[0].length == 0) return false;
    if (word == null || word.length() == 0) return true;

    int l = board.length;
    int w = board[0].length;

    for (int i=0; i<l; i++) {
        for (int j=0; j<w; j++) {
            if (board[i][j] == word.charAt(0) && util(board, new boolean[l][w], i, j, word, 0)) {
                return true;
            }
        }
    }

    return false;
}
```

## Palindrome partitioning

```java
public List<List<String>> partition(String s) {
   List<List<String>> list = new ArrayList<>();
   backtrack(list, new ArrayList<>(), s, 0);
   return list;
}

public void backtrack(List<List<String>> list, List<String> tempList, String s, int start){
   if(start == s.length())
      list.add(new ArrayList<>(tempList));
   else{
      for(int i = start; i < s.length(); i++){
         if(isPalindrome(s, start, i)){
            tempList.add(s.substring(start, i + 1));
            backtrack(list, tempList, s, i + 1);
            tempList.remove(tempList.size() - 1);
         }
      }
   }
}

public boolean isPalindrome(String s, int low, int high){
   while(low < high)
      if(s.charAt(low++) != s.charAt(high--)) return false;
   return true;
}
```

## Robot clean the room

Given functions:

1. `boolean move()`
2. `void clean()`
3. `void turnRight()`
4. `void turnLeft()`

__My solution:__

```java
// private fields:

Robot robot;
int[][] deltas = new int[][]{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}; //clockwise deltas to be added in x,y
Map<Integer, Set<Integer>> visited = new HashMap<>();

// utility methods:

boolean visited(int x, int y) {
    return visited.containsKey(x) && visited.get(x).contains(y);
}

void visit(int x, int y) {
    visited.putIfAbsent(x, new HashSet<>());
    visited.get(x).add(y);
}

void goBackAndTurnForward() {
    robot.turnRight();
    robot.turnRight();
    robot.move();
    robot.turnRight();
    robot.turnRight();
}

// main backtracking method:

void backTrack(int x, int y, int dir) {
    visit(x, y);
    robot.clean();

    for (int i=0; i<4; i++) {
        int newDir = (dir + i) % 4;
        int newX = x + deltas[newDir][0]; //next spot calculation
        int newY = y + deltas[newDir][1];

        if (!visited(newX, newY) && robot.move()) {
          //if next spot is not visited and can move there
            backTrack(newX, newY, newDir);
            goBackAndTurnForward(); //backtracking
        }

        robot.turnRight(); // next direction clockwise
    }
}

public void cleanRoom(Robot robot) {
    this.robot = robot;
    backTrack(0, 0, 0);
}
```

## Split a String Into the Max Number of Unique Substrings

```java
private int backtrackDFS(String s, int i, Set<String> set) {
    int res = set.size();

    for (int j=i+1; j<=s.length(); j++) {
        String sub = s.substring(i, j);
        if (set.contains(sub)) {
            continue;
        }
        set.add(sub);

        res = Math.max(res, backtrack(s, j, set));

        set.remove(sub);
    }

    return res;
}

public int maxUniqueSplit(String s) {
    Set<String> set = new HashSet<>();

    return backtrackDFS(s, 0, set);
}
```

## Combination Sum, can have any repeated candidates

Example:

Input : [2,3,6,7], 7
Output : [[2,2,3], [7]]

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> res = new ArrayList<>();
    Arrays.sort(candidates);
    backtrack(candidates, candidates.length-1, target, 0, new LinkedList<>(), res);
    return res;
}

private void backtrack(int[] sorted, int i, int target,
                        int sum, LinkedList<Integer> list, List<List<Integer>> res) {
    if (sum == target) {
        res.add(new ArrayList<>(list));
    } else if (sum < target) {
        for (int j=i; j>=0; j--) {
            list.add(sorted[j]);
            backtrack(sorted, j, target, sum + sorted[j], list, res);
            list.removeLast();
        }
    }
}
```

## Combinations Sum - containing duplicates

Use duplicates algo from permutations, and combinations algo for overall structure.

```java
public List<List<Integer>> combinationSum2(int[] candidates, int target) {
    List<List<Integer>> res = new ArrayList<>();
    Arrays.sort(candidates);
    backtrack(candidates, -1, target, 0,
              new boolean[candidates.length], new LinkedList<>(), res);
    return res;
}

private void backtrack(int[] sorted, int i, int target, int sum,
                        boolean[] visited, LinkedList<Integer> list, List<List<Integer>> res) {
    if (sum == target) {
        res.add(new ArrayList<>(list));
    } else if (sum < target) {
        for (int j=i+1; j<sorted.length; j++) {
            if (visited[j] || j > 0 && sorted[j] == sorted[j-1] && !visited[j-1]) continue;
            visited[j] = true;
            list.add(sorted[j]);
            backtrack(sorted, j, target, sum + sorted[j], visited, list, res);
            list.removeLast();
            visited[j] = false;
        }
    }
}
```

### Sudoku Solver

```java
public void solveSudoku(char[][] board) {
    doSolve(board, 0, 0);
}

private boolean doSolve(char[][] board, int row, int col) {
    // note: must reset col here!
    for (int i = row; i < 9; i++, col = 0) {
        for (int j = col; j < 9; j++) {
            if (board[i][j] != '.') continue;
            for (char num = '1'; num <= '9'; num++) {
                if (isValid(board, i, j, num)) {
                    board[i][j] = num;
                    if (doSolve(board, i, j + 1))
                        return true;
                    board[i][j] = '.';
                }
            }
            return false;
        }
    }
    return true;
}

private boolean isValid(char[][] board, int row, int col, char num) {
    // Block no. is i/3, first element is i/3*3
    int blkrow = (row / 3) * 3, blkcol = (col / 3) * 3;
    for (int i = 0; i < 9; i++)
        if (board[i][col] == num || board[row][i] == num ||
                board[blkrow + i / 3][blkcol + i % 3] == num)
            return false;
    return true;
}
```
