package com.npuzzle;

import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class Solver {

  public Node start, goal;

  public Solver(Node start, Node goal) {
    this.start = start;
    this.goal = goal;
  }

  public Node ida() {
    int bound = this.start.f();
    int nextBound;

    while (true) {
      PriorityQueue<Node> queue = new PriorityQueue<>(new Compare());
      ArrayList<Node> path = new ArrayList<>();
      path.add(0, this.start);
      nextBound = search(path, queue, bound);

      if (nextBound == 0) return queue.poll();

      bound = nextBound;
    }
  }

  public int search(ArrayList<Node> path, PriorityQueue<Node> queue, int bound) {
    Node currentNode = path.get(path.size() - 1);

    if (currentNode.f() > bound) {
      queue.add(currentNode);
      return currentNode.f();
    }

    if (isGoal(currentNode)) {
      queue.clear();
      queue.add(currentNode);
      return 0;
    }

    ArrayList<Node> neighbors = currentNode.neighbors();

    for (Node neighbor: neighbors) {
      if (!path.contains(neighbor)) {
        if (currentNode.parent != null && currentNode.parent.board.isEqual(neighbor.board)) continue;

        path.add(neighbor);
        int result = search(path, queue, bound);

        if (result == 0) {
          return 0;
        }

        path.remove(path.size() - 1);
      }
    }

    return queue.peek().f();
  }

  public boolean isGoal(Node node) {
    for (int row = 0; row < this.size(); row++) {
      for (int col = 0; col < this.size(); col++) {
        if (node.board.tileAt(row, col) != this.goal.board.tileAt(row, col)) return false;
      }
    }

    return true;
  }

  private int size() {
    return this.start.board.size();
  }

  public boolean isSolvable() {
    int n = this.size();
    boolean isSolvable;
    int inversions = this.getInversions();

    if (n % 2 == 0) {
      isSolvable = (inversions + this.start.board.getZeroPosition().get("row")) % 2 != 0;
    } else {
      isSolvable = inversions % 2 == 0;
    }

    return isSolvable;
  }

  private int getInversions() {
    int count = 0;
    int n = this.size() * this.size() - 1;
    int[] startTiles = Stream.of(this.start.board.tiles)
            .flatMapToInt(IntStream::of)
            .filter(number -> number != 0)
            .toArray();

    for (int i = 0; i < n; i++) {
      for (int j = i + 1; j < n; j++) {
        if (startTiles[i] > startTiles[j]) count++;
      }
    }

    return count;
  }
}
