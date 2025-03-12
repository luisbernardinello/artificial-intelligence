package com.nqueens;

import java.util.HashMap;
import java.util.Random;

public class Solver {
  private final int n;
  private final int[] queens;
  final int[] solution;
  private final ConflictManager conflictManager;
  private final BoardInitStrategy initStrategy;
  private final Random rand;
  public int moves;

  Solver(int n, BoardInitStrategy initStrategy, Random rand) {
      this.n = n;
      this.queens = new int[n];
      this.solution = new int[n];
      this.rand = rand;
      this.conflictManager = new ConflictManager(n, queens, rand);
      this.initStrategy = initStrategy;
      this.moves = 0;
  }

  public void solve() {
      do {
          reset();
          initStrategy.initialize(queens, n);
          conflictManager.setConflicts();

          if (!conflictManager.hasConflicts()) {
              System.arraycopy(queens, 0, solution, 0, n);
              break;
          }

          search();
      } while (conflictManager.hasConflicts());
  }

  private void search() {
      int iter = 0;
      while (iter < n) {
          moves++;
          HashMap<String, Integer> colMaxConflictsData = conflictManager.getColumnMaxConflicts();
          int colMaxConflicts = colMaxConflictsData.get("col");
          int currentConflicts = colMaxConflictsData.get("conflicts");

          HashMap<String, Integer> rowMinConflictsData = conflictManager.findMinConflictsRow(colMaxConflicts, queens[colMaxConflicts]);
          int rowMinConflicts = rowMinConflictsData.get("row");
          int minConflicts = rowMinConflictsData.get("conflicts");

          int oldRow = queens[colMaxConflicts];
          int newRow = rowMinConflicts;

          if (currentConflicts == minConflicts) {
              int randomRow;
              do {
                  randomRow = rand.nextInt(n);
                  newRow = randomRow;
              } while (randomRow == queens[colMaxConflicts]);

              queens[colMaxConflicts] = randomRow;
          } else if (currentConflicts > minConflicts) {
              queens[colMaxConflicts] = rowMinConflicts;
          } else {
              break;
          }

          conflictManager.updateConflicts(colMaxConflicts, oldRow, newRow);

          if (!conflictManager.hasConflicts()) {
              System.arraycopy(queens, 0, solution, 0, n);
              break;
          }

          iter++;
      }
  }

  private void reset() {
      for (int i = 0; i < n; i++) {
          queens[i] = 0;
      }
      conflictManager.resetConflicts();
  }

  public void print(int[] queens) {
      System.out.println();
      for (int row = 0; row < n; row++) {
          for (int col = 0; col < n; col++) {
              if (queens[col] == row) {
                  System.out.print("* ");
              } else {
                  System.out.print("_ ");
              }
          }
          System.out.println();
      }
  }
}