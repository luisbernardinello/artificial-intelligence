package com.ticTacToe;

import java.util.ArrayList;
import java.util.List;

public class GameBoard {
    public static final int EMPTY = 0;
    public static final int X_PLAYER = 1;
    public static final int O_PLAYER = -1;
    public static final int BOARD_SIZE = 3;
    public static final int TOTAL_CELLS = BOARD_SIZE * BOARD_SIZE;
    
    private int[][] board;
    private int filledCells;
    
    public GameBoard() {
        board = new int[BOARD_SIZE][BOARD_SIZE];
        filledCells = 0;
    }
    
    // Método para criar uma deep copy do tabuleiro (útil para o minimax)
    public GameBoard copy() {
        GameBoard newBoard = new GameBoard();
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] != EMPTY) {
                    newBoard.setCell(i, j, board[i][j]);
                }
            }
        }
        return newBoard;
    }
    
    public int[][] getBoard() {
        return board;
    }
    
    public void setCell(int row, int col, int player) {
        if (board[row][col] == EMPTY && player != EMPTY) {
            filledCells++;
        } else if (board[row][col] != EMPTY && player == EMPTY) {
            filledCells--;
        }
        board[row][col] = player;
    }
    
    public int getCell(int row, int col) {
        return board[row][col];
    }
    
    public int getFilledCells() {
        return filledCells;
    }
    
    public List<Cell> getEmptyCells() {
        List<Cell> emptyCells = new ArrayList<>();
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    emptyCells.add(new Cell(i, j));
                }
            }
        }
        return emptyCells;
    }
    
    public boolean isFull() {
        return filledCells == TOTAL_CELLS;
    }
    
    public boolean isEmpty() {
        return filledCells == 0;
    }
    
    public int getCurrentPlayer() {
        int xCount = 0;
        int oCount = 0;
        
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == X_PLAYER) {
                    xCount++;
                } else if (board[i][j] == O_PLAYER) {
                    oCount++;
                }
            }
        }
        
        return xCount <= oCount ? X_PLAYER : O_PLAYER;
    }
    
    public void printBoard() {
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                char symbol;
                if (board[i][j] == X_PLAYER) {
                    symbol = 'X';
                } else if (board[i][j] == O_PLAYER) {
                    symbol = 'O';
                } else {
                    symbol = '_';
                }
                System.out.print(symbol);
                if (j < BOARD_SIZE - 1) {
                    System.out.print(" | ");
                }
            }
            System.out.println();
            if (i < BOARD_SIZE - 1) {
                System.out.println("---------");
            }
        }
        System.out.println();
    }
}
