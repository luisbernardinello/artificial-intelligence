# N Queens

The N queens puzzle is the problem of placing N chess queens on an N×N chessboard so that no two queens threaten each other, 
thus a solution requires that no two queens share the same row, column, or diagonal. 

\* *Requirement - to work for N = 10 000 (for under a second)*

## Solution
***Hill Climbing*** and ***MinConflicts*** algorithms.

### Input

* N - integer, the number of queens to be placed

#### Example
```
4
```

### Output

* print the solution board by marking queens with *, and empty spaces on the board with _. _(For larger boards, print only the time spent on solving the problem or the number of moves made.)_

#### Example
```
_  *   _  _

_  _  _  * 

*   _  _  _

_  _  *   _
```
