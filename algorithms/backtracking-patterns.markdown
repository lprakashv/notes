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
