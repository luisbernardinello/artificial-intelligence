package com.ticTacToe;

public class TicTacToeEvaluator implements BoardEvaluator {
    @Override
    public int evaluate(GameBoard board) {
        // Verifica se exite um vencedor
        if (checkWinner(board, GameBoard.X_PLAYER)) {
            return 1;
        } else if (checkWinner(board, GameBoard.O_PLAYER)) {
            return -1;
        }
        return 0;
    }
    
    @Override
    public boolean isTerminal(GameBoard board) {
        // Um estado é terminal se EXISTE um vencedor ou o tabuleiro está cheio
        return checkWinner(board, GameBoard.X_PLAYER) ||
               checkWinner(board, GameBoard.O_PLAYER) ||
               board.isFull() ||
               board.getEmptyCells().isEmpty();
    }
    
    private boolean checkWinner(GameBoard board, int player) {
        int[][] boardArray = board.getBoard();
        
        // Verifica linhas
        for (int i = 0; i < GameBoard.BOARD_SIZE; i++) {
            if (boardArray[i][0] == player && 
                boardArray[i][0] == boardArray[i][1] && 
                boardArray[i][1] == boardArray[i][2]) {
                return true;
            }
        }
        
        // Verifica colunas
        for (int j = 0; j < GameBoard.BOARD_SIZE; j++) {
            if (boardArray[0][j] == player && 
                boardArray[0][j] == boardArray[1][j] && 
                boardArray[1][j] == boardArray[2][j]) {
                return true;
            }
        }
        
        // Verifica diagonais
        if (boardArray[0][0] == player && 
            boardArray[0][0] == boardArray[1][1] && 
            boardArray[1][1] == boardArray[2][2]) {
            return true;
        }
        
        if (boardArray[0][2] == player && 
            boardArray[0][2] == boardArray[1][1] && 
            boardArray[1][1] == boardArray[2][0]) {
            return true;
        }
        
        return false;
    }
}