package com.npuzzle;

import java.util.HashMap;

public class Board {

  public int[][] tiles;
  int zero;

  public Board(int[][] tiles) {
    this.tiles = tiles;
  }

  public Board(int[][] tiles, int zero) {
    this.tiles = tiles;
    this.zero = zero;
  }

  public int size() {
    return this.tiles.length;
  }

  public HashMap<String, Board> neighbors() {
    HashMap<String, Board> neighbors = new HashMap<>();
    HashMap<String, Integer> zero = this.getZeroPosition();
    int currentZeroRow = zero.get("row");
    int currentZeroCol = zero.get("col");

    HashMap<String, HashMap<String, Integer>> directions = this.getDirectionsCoordinates();
    directions.forEach((direction, coordinates) -> {
      this.addNeighbor(neighbors, currentZeroRow, currentZeroCol, direction, coordinates);
    });

    return neighbors;
  }

  private HashMap<String, HashMap<String, Integer>> getDirectionsCoordinates() {
    HashMap<String, HashMap<String, Integer>> coordinates = new HashMap<>();

    HashMap<String, Integer> leftCoordinates = new HashMap<>();
    leftCoordinates.put("row", 0);
    leftCoordinates.put("col", 1);
    coordinates.put("left", leftCoordinates);

    HashMap<String, Integer> rightCoordinates = new HashMap<>();
    rightCoordinates.put("row", 0);
    rightCoordinates.put("col", -1);
    coordinates.put("right", rightCoordinates);

    HashMap<String, Integer> upCoordinates = new HashMap<>();
    upCoordinates.put("row", 1);
    upCoordinates.put("col", 0);
    coordinates.put("up", upCoordinates);

    HashMap<String, Integer> downCoordinates = new HashMap<>();
    downCoordinates.put("row", -1);
    downCoordinates.put("col", 0);
    coordinates.put("down", downCoordinates);

    return coordinates;
  }

  private void addNeighbor(HashMap<String, Board> neighbors, int currentZeroRow, int currentZeroCol, String direction, HashMap<String, Integer> directionCoordinates) {
    int newZeroRow = currentZeroRow + directionCoordinates.get("row");
    int newZeroCol = currentZeroCol + directionCoordinates.get("col");

    if (this.zeroInsideBoard(newZeroRow, newZeroCol)) {
      Board neighborBoard = this.getNeighborBoard(currentZeroRow, currentZeroCol, newZeroRow, newZeroCol);
      neighbors.put(direction, neighborBoard);
    }
  }

  private Board getNeighborBoard(int currentZeroRow, int currentZeroCol, int newZeroRow, int newZeroCol) {
    int tile = this.tileAt(newZeroRow, newZeroCol);
    int[][] copyTiles = new int[this.size()][this.size()];
    for (int i = 0; i < this.size(); i++) {
      System.arraycopy(this.tiles[i], 0, copyTiles[i], 0, this.size());
    }

    Board neighbor = new Board(copyTiles);
    neighbor.setTileAt(newZeroRow, newZeroCol, 0);
    neighbor.setTileAt(currentZeroRow, currentZeroCol, tile);

    return neighbor;
  }

  public boolean isEqual(Board board) {
    for (int row = 0; row < this.size(); row++) {
      for (int col = 0; col < this.size(); col++) {
        if (this.tileAt(row, col) != board.tileAt(row, col)) return false;
      }
    }

    return true;
  }

  public int tileAt(int row, int col) {
    return this.tiles[row][col];
  }

  private void setTileAt(int row, int col, int tile) {
    this.tiles[row][col] = tile;
  }

  private boolean zeroInsideBoard(int row, int col) {
    return row >= 0 && row < this.size() && col >= 0 && col < this.size();
  }

  public HashMap<String, Integer> getZeroPosition() {
    HashMap<String, Integer> coordinates = new HashMap<>();

    for (int row = 0; row < this.size(); row++) {
      for (int col = 0; col < this.size(); col++) {
        if (this.tileAt(row, col) == 0) {
          coordinates.put("row", row);
          coordinates.put("col", col);
          return coordinates;
        }
      }
    }

    return coordinates;
  }
}

