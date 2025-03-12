package com.ticTacToe;

import java.util.Arrays;
import java.util.List;

public class Main {
  public static void main(String[] args) {
      // Tabuleiros para experimentos
      GameBoard jogo1 = new GameBoard();
      jogo1.setCell(0, 0, GameBoard.X_PLAYER);
      jogo1.setCell(0, 1, GameBoard.O_PLAYER);
      jogo1.setCell(0, 2, GameBoard.X_PLAYER);
      jogo1.setCell(1, 0, GameBoard.O_PLAYER);
      jogo1.setCell(1, 1, GameBoard.X_PLAYER);
      jogo1.setCell(1, 2, GameBoard.O_PLAYER);
      
      GameBoard jogo2 = new GameBoard();
      jogo2.setCell(0, 0, GameBoard.X_PLAYER);
      jogo2.setCell(0, 1, GameBoard.O_PLAYER);
      jogo2.setCell(0, 2, GameBoard.X_PLAYER);
      jogo2.setCell(1, 0, GameBoard.O_PLAYER);
      jogo2.setCell(1, 1, GameBoard.O_PLAYER);
      jogo2.setCell(1, 2, GameBoard.X_PLAYER);
      
      GameBoard jogo3 = new GameBoard();
      jogo3.setCell(0, 0, GameBoard.O_PLAYER);
      jogo3.setCell(0, 2, GameBoard.X_PLAYER);
      jogo3.setCell(1, 1, GameBoard.X_PLAYER);
      jogo3.setCell(2, 0, GameBoard.O_PLAYER);
      
      // Lista de experimentos
      List<GameBoard> experiments = Arrays.asList(jogo1, jogo2, jogo3);
      
      // Executa experimentos
      for (int i = 0; i < experiments.size(); i++) {
          System.out.println("Experimento " + (i + 1) + ":\n");
          System.out.println("Estado inicial:");
          experiments.get(i).printBoard();
          
          // Cria o controlador e executar o minimax
          GameController controller = new GameController();
          MinimaxResult result = controller.executeMinimaxExperiment(experiments.get(i), true);
          
          System.out.println("Estado final depois de executar o Minimax:");
          result.getBoard().printBoard();
          System.out.println("Nodes expandidos: " + result.getExpandedNodes());
          
          System.out.println("------------------------------------------");
      }
  }
}