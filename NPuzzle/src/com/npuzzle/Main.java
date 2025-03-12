package com.npuzzle;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;

public class Main {

  public static void main(String[] args) throws IOException {
    InputReader reader = new InputReader();
    reader.read();

    Board startBoard = new Board(reader.startBoardTiles);
    Board goalBoard = new Board(reader.goalBoardTiles, reader.I);

    Node startNode = new Node(startBoard, null, goalBoard, 0, null);
    Node goalNode = new Node(goalBoard, null, goalBoard, 0, null);

    Solver solver = new Solver(startNode, goalNode);
    boolean isSolvable = solver.isSolvable();

    if (isSolvable) {
      Node solutionNode;

      if (solver.isGoal(startNode)) {
        solutionNode = startNode;
      } else {
        Instant start = Instant.now();
        solutionNode = solver.ida();
        Instant finish = Instant.now();

        long timeElapsed = Duration.between(start, finish).toSeconds();
        System.out.println("Time elapsed: " + timeElapsed);
      }

      System.out.println(solutionNode.g);
      ArrayList<Node> pathToSolution = solutionNode.getPathToRoot();
      pathToSolution.forEach(node -> {
        if (node.move != null) System.out.println(node.move);
      });
    } else {
      System.out.print("Board is not solvable!");
    }
  }
}

