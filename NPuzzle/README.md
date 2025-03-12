# N Puzzle

## Problem
The N-puzzle is a sliding puzzle that is played on a N-by-N grid with N-1 square tiles labeled 1 through N-1, plus a blank square. 
The goal is to rearrange the tiles so that they are in row-major order, using as few moves as possible. 
You are permitted to slide tiles either horizontally or vertically into the blank square.

## Solution 
Used the ***IDA**** algorithm and the ***Manhattan Distance*** heuristic.

### Input
* N - the number of tiles (8, 15, 24, etc.)
* I - the index position of the blank tile (represented with zero in the board) in the solution (when -1 the index is set by default in the lowest right)

#### Example
```
8 
-1
4 1 3
7 2 6
5 8 0
```

### Output
* The number of moves of the optimal solution from the start to the goal board
* The moves made to get to the goal state by moving a tile to the blank space (left, right, up and down)

#### Example
```
8
right
right
down
down
left
up
up
left
```
