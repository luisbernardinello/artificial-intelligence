package com.nqueens;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

// Singleton para gerenciamento de conflitos
public class ConflictManager {
    private final int n;
    private final int[] queens;
    private int[] rowConflicts;
    private int[] d1Conflicts;
    private int[] d2Conflicts;
    private final Random rand;

    ConflictManager(int n, int[] queens, Random rand) {
        this.n = n;
        this.queens = queens;
        this.rand = rand;
        this.rowConflicts = new int[n];
        this.d1Conflicts = new int[2 * n - 1];
        this.d2Conflicts = new int[2 * n - 1];
    }

    void setConflicts() {
        resetConflicts();

        for (int i = 0; i < n; i++) {
            rowConflicts[queens[i]]++;
            d1Conflicts[n - 1 + i - queens[i]]++;
            d2Conflicts[queens[i] + i]++;
        }
    }

    void resetConflicts() {
        rowConflicts = new int[n];
        d1Conflicts = new int[2 * n - 1];
        d2Conflicts = new int[2 * n - 1];
    }

    void updateConflicts(int col, int oldRow, int newRow) {
        removeConflicts(col, oldRow);
        addConflicts(col, newRow);
    }

    void removeConflicts(int col, int row) {
        rowConflicts[row]--;
        d1Conflicts[n - 1 + col - row]--;
        d2Conflicts[col + row]--;
    }

    void addConflicts(int col, int row) {
        rowConflicts[row]++;
        d1Conflicts[n - 1 + col - row]++;
        d2Conflicts[col + row]++;
    }

    HashMap<String, Integer> getColumnMaxConflicts() {
        int maxConflicts = Integer.MIN_VALUE;
        List<Integer> maxConflictsColumns = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            int currentConflicts = getConflictsForQueen(i, queens[i]);
            if (currentConflicts == maxConflicts) {
                maxConflictsColumns.add(i);
            }

            if (currentConflicts > maxConflicts) {
                maxConflicts = currentConflicts;
                maxConflictsColumns.clear();
                maxConflictsColumns.add(i);
            }
        }

        int columnIndex = 0;
        if (maxConflictsColumns.size() > 1) {
            columnIndex = rand.nextInt(maxConflictsColumns.size());
        }

        int maxCol = maxConflictsColumns.get(columnIndex);
        HashMap<String, Integer> columnMaxConflicts = new HashMap<>();
        columnMaxConflicts.put("col", maxCol);
        columnMaxConflicts.put("conflicts", maxConflicts);
        return columnMaxConflicts;
    }

    HashMap<String, Integer> findMinConflictsRow(int queenCol, int queenRow) {
        int minConflicts = Integer.MAX_VALUE;
        List<Integer> minRows = new ArrayList<>();

        for (int row = 0; row < n; row++) {
            if (row == queenRow) continue;

            int newRowConflicts = (rowConflicts[row] + 1) / 2;
            int newD1Conflicts = (d1Conflicts[n - 1 + queenCol - row] + 1) / 2;
            int newD2Conflicts = (d2Conflicts[queenCol + row] + 1) / 2;
            int newConflicts = newRowConflicts + newD1Conflicts + newD2Conflicts;

            if (minConflicts == newConflicts) {
                minRows.add(row);
            }

            if (newConflicts < minConflicts) {
                minConflicts = newConflicts;
                minRows.clear();
                minRows.add(row);
            }
        }

        int rowIndex = 0;
        if (minRows.size() > 1) {
            rowIndex = rand.nextInt(minRows.size());
        }

        int minRow = minRows.get(rowIndex);
        HashMap<String, Integer> rowMinConflicts = new HashMap<>();
        rowMinConflicts.put("row", minRow);
        rowMinConflicts.put("conflicts", minConflicts);
        return rowMinConflicts;
    }

    int getConflictsForQueen(int col, int row) {
        int currentQueenOccurrences = 0;
        int rowConflictQueens = rowConflicts[row];
        int d1ConflictQueens = d1Conflicts[n - 1 + row - col];
        int d2ConflictQueens = d2Conflicts[row + col];

        int conflicts = rowConflictQueens + d1ConflictQueens + d2ConflictQueens;
        if (rowConflictQueens != 0) {
            currentQueenOccurrences++;
        }
        if (d1ConflictQueens != 0) {
            currentQueenOccurrences++;
        }
        if (d2ConflictQueens != 0) {
            currentQueenOccurrences++;
        }

        conflicts -= currentQueenOccurrences;
        return conflicts;
    }

    boolean hasConflicts() {
        for (int i = 0; i < n; i++) {
            if (i < n) {
                if (rowConflicts[queens[i]] > 1) {
                    return true;
                }
            }

            if (d1Conflicts[n - 1 + i - queens[i]] > 1 || d2Conflicts[queens[i] + i] > 1) {
                return true;
            }
        }

        return false;
    }
}