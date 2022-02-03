# Backtracking

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

Example N - queens:

```python
def backtrack_nqueen(row = 0, count = 0):
    for col in range(n):
        # iterate through columns at the curent row.
        if is_not_under_attack(row, col):
            # explore this partial candidate solution, and mark the attacking zone
            place_queen(row, col)
            if row + 1 == n:
                # we reach the bottom, i.e. we find a solution!
                count += 1
            else:
                # we move on to the next row
                count = backtrack_nqueen(row + 1, count)
            # backtrack, i.e. remove the queen and remove the attacking zone.
            remove_queen(row, col)
    return count
```
