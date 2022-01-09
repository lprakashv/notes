# Backtracking Problem patterns

- Form of recursion.
- We incrementally build candidates to the solutions.
  - If partial candidate cannot be completed to a valid solutions, we abandon it.
- Much faster than brute-force (enumeration of all complete candidates), because it can eliminate large no of candidates with a single test.
- Kind of __similar to DFS__
- General algorithm for finding __all solutions to some computation__ -> __constraint satisfaction problems__
- Examples:
  - 8-queens
  - sudoku
  - ...

General Pattern:

```python
def backtracking(chosen):
   if valid_solution?(chosen):
      perform_action_with(chosen)        # save, print, etc
   else:
      for _each_option_ in _we_can_take_here_:
         chosen = choose_one(_each_option_)     # choose
         backtracking(_each_option_)            # explore
         chosen = unchoose(_each_option_)       # unchoose
```

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
Int numQueens;

Void solve() {
  setQueens(0); // start with 0th column
  printTable();
}

Boolean setQueens(int col) {
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
