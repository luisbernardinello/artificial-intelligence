package com.nqueens;

import java.util.Random;

public class StaircaseInitStrategy implements BoardInitStrategy {
    private final Random rand;

    StaircaseInitStrategy(Random rand) {
        this.rand = rand;
    }

    @Override
    public void initialize(int[] queens, int n) {
        if (n % 6 == 2) {
            set2or3RemainderBoard(queens, n, n - 4, n - 3);
        } else if (n % 6 == 3) {
            set2or3RemainderBoard(queens, n, n - 4, n - 1);
        } else {
            setOtherRemainderBoard(queens, n);
        }
    }

    private void set2or3RemainderBoard(int[] queens, int n, int firstCount, int secondCount) {
        for (int i = 0; i < n / 2 - 1; i++) {
            queens[i] = firstCount;
            firstCount -= 2;
        }

        queens[n - 1] = pickRandom(n);

        for (int i = n / 2 + 1; i < n; i++) {
            queens[i] = secondCount;
            secondCount -= 2;
        }

        queens[n / 2] = pickRandom(n);
    }

    private void setOtherRemainderBoard(int[] queens, int n) {
        int c = 0;

        for (int i = 0; i < n / 2; i++) {
            queens[n - 1 - i - n / 2] = c;
            queens[n - i - 1] = c + 1;
            c += 2;
        }
    }

    private int pickRandom(int max) {
        return rand.nextInt(max);
    }
}