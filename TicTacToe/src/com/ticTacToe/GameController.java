package com.ticTacToe;

import java.util.ArrayList;
import java.util.List;

public class GameController {
    private BoardEvaluator evaluator;
    
    public GameController() {
        this.evaluator = new TicTacToeEvaluator();
    }
    
    public MinimaxResult executeMinimaxExperiment(GameBoard initialBoard, boolean maximizing) {
        // Cria o nó raiz para o minimax
        Node root = new Node(initialBoard);
        List<Node> unexploredNodes = new ArrayList<>();
        unexploredNodes.add(root);
        int expandedNodes = 0;
        
        // Expannde árvore
        while (!unexploredNodes.isEmpty()) {
            Node node = unexploredNodes.remove(unexploredNodes.size() - 1);
            expandedNodes++;
            
            if (evaluator.isTerminal(node.getBoard())) {
                // Se for um nó folha, avalia o tabuleiro
                node.setValue(evaluator.evaluate(node.getBoard()));
            } else {
                // Se não , gera os movimentos possíveis
                int currentPlayer = node.getBoard().getCurrentPlayer();
                List<Cell> validMoves = node.getBoard().getEmptyCells();
                
                for (Cell move : validMoves) {
                    // Para cada movimento que for válido, gera um novo estado e cria um nó filho
                    GameBoard newBoard = node.getBoard().copy();
                    newBoard.setCell(move.getRow(), move.getCol(), currentPlayer);
                    
                    Node childNode = new Node(newBoard, move, node);
                    node.addChild(childNode);
                    unexploredNodes.add(childNode);
                }
            }
        }
        
        // Calcula o melhor valor com minimax
        int bestValue = getBestValue(root, maximizing);
        
        // Encontra o tabuleiro final com o melhor valor
        GameBoard finalBoard = null;
        for (Node child : root.getChildren()) {
            if (child.getValue() == bestValue) {
                finalBoard = child.getBoard();
                break;
            }
        }
        
        return new MinimaxResult(finalBoard, expandedNodes);
    }
    
    private int getBestValue(Node node, boolean maximizing) {
        if (node.getValue() != null) {
            return node.getValue();
        }
        
        if (maximizing) {
            int maxValue = Integer.MIN_VALUE;
            for (Node child : node.getChildren()) {
                int value = getBestValue(child, false);
                maxValue = Math.max(maxValue, value);
            }
            node.setValue(maxValue);
            return maxValue;
        } else {
            int minValue = Integer.MAX_VALUE;
            for (Node child : node.getChildren()) {
                int value = getBestValue(child, true);
                minValue = Math.min(minValue, value);
            }
            node.setValue(minValue);
            return minValue;
        }
    }
}