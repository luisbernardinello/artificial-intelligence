package com.ticTacToe;

public class MinimaxResult {
    private final GameBoard board;
    private final int expandedNodes;
    
    public MinimaxResult(GameBoard board, int expandedNodes) {
        this.board = board;
        this.expandedNodes = expandedNodes;
    }
    
    public GameBoard getBoard() {
        return board;
    }
    
    public int getExpandedNodes() {
        return expandedNodes;
    }
}
