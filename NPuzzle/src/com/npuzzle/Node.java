package com.npuzzle;

import java.util.ArrayList;
import java.util.HashMap;

public class Node {

  public String move;
  public Node parent;
  public Board board, goal;
  public int g, manhattanDistance;

  public Node(Board board, Node parent, Board goal, int g, String move) {
    this.board = board;
    this.parent = parent;
    this.goal = goal;
    this.g = g;
    this.move = move;
    this.manhattanDistance = this.manhattanDistance();
  }

  public int f() {
    return this.g + this.manhattanDistance;
  }

  public int manhattanDistance() {
    int manhattan = 0;

    for (int row = 0; row < this.size(); row++) {
      for (int col = 0; col < this.size(); col++) {
        manhattan += this.getTileDistance(this.board.tileAt(row, col), row, col);
      }
    }

    return manhattan;
  }

  public int getTileDistance(int tileNumber, int tileRow, int tileCol) {
    if (tileNumber == 0) return 0;
    tileNumber -= 1;

    if (this.goal.zero != -1 && tileNumber >= this.goal.zero) tileNumber += 1;

    int goalRow = tileNumber / this.size();
    int goalCol = tileNumber % this.size();
    int distance = Math.abs(tileRow - goalRow) + Math.abs(tileCol - goalCol);

    return distance;
  }

  public ArrayList<Node> neighbors() {
    ArrayList<Node> neighbors = new ArrayList<>();

    HashMap<String, Board> neighborBoards = this.board.neighbors();
    neighborBoards.forEach((move, neighborBoard) -> {
      Node node = new Node(neighborBoard, this, this.goal, this.g + 1, move);
      neighbors.add(node);
    });

    return neighbors;
  }

  public ArrayList<Node> getPathToRoot() {
    ArrayList<Node> path = new ArrayList<>();
    Node node = this;
    path.add(node);

    while (node.parent != null) {
      path.add(0, node.parent);
      node = node.parent;
    }

    return path;
  }

  private int size() {
    return this.board.size();
  }
}
