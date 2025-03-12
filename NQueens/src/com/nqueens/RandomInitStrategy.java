package com.nqueens;

import java.util.HashMap;
import java.util.Random;

public class RandomInitStrategy implements BoardInitStrategy {
    private final Random rand;
    private final ConflictManager conflictManager;

    RandomInitStrategy(Random rand, ConflictManager conflictManager) {
        this.rand = rand;
        this.conflictManager = conflictManager;
    }

    @Override
    public void initialize(int[] queens, int n) {
        for (int i = 0; i < n; i++) {
            queens[i] = Integer.MIN_VALUE;
        }

        int randomFirstRow = rand.nextInt(n);
        queens[0] = randomFirstRow;
        conflictManager.addConflicts(0, randomFirstRow);

        for (int i = 1; i < n; i++) {
            HashMap<String, Integer> minRowData = conflictManager.findMinConflictsRow(i, -1);
            int row = minRowData.get("row");
            queens[i] = row;
            conflictManager.addConflicts(i, row);
        }
    }
}
