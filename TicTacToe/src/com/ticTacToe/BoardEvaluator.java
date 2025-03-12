package com.ticTacToe;

public interface BoardEvaluator {
    int evaluate(GameBoard board);
    boolean isTerminal(GameBoard board);
}
