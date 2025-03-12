package com.ticTacToe;

import java.util.ArrayList;
import java.util.List;

public class Node {
    private GameBoard board;
    private Cell move;
    private Node parent;
    private List<Node> children;
    private Integer value;
    
    public Node(GameBoard board) {
        this.board = board;
        this.children = new ArrayList<>();
        this.value = null;
    }
    
    public Node(GameBoard board, Cell move, Node parent) {
        this(board);
        this.move = move;
        this.parent = parent;
    }
    
    public GameBoard getBoard() {
        return board;
    }
    
    public Cell getMove() {
        return move;
    }
    
    public Node getParent() {
        return parent;
    }
    
    public List<Node> getChildren() {
        return children;
    }
    
    public void addChild(Node child) {
        children.add(child);
    }
    
    public Integer getValue() {
        return value;
    }
    
    public void setValue(Integer value) {
        this.value = value;
    }
}

