package com.nqueens;

import java.util.Random;

// Builder Pattern para configuração do Solver
public class SolverBuilder {
    private int n;
    private BoardInitStrategy initStrategy;
    private Random rand;

    SolverBuilder(int n) {
        this.n = n;
        this.rand = new Random();
    }

    SolverBuilder withBoardInitStrategy(BoardInitStrategy initStrategy) {
        this.initStrategy = initStrategy;
        return this;
    }

    SolverBuilder withRandomSeed(long seed) {
        this.rand = new Random(seed);
        return this;
    }

    Solver build() {
        return new Solver(n, initStrategy, rand);
    }
}