package com.ticTacToe;

public class Cell {
  int row;
  int col;
  
  public Cell(int row, int col) {
      this.row = row;
      this.col = col;
  }
  
  public int getRow() {
      return row;
  }
  
  public int getCol() {
      return col;
  }
}