package com.TravellingSalesmanProblem;

import java.text.DecimalFormat;

public class Gene {

  public int x, y;
  public String name;

  public Gene(int x, int y, String name) {
    this.x = x;
    this.y = y;
    this.name = name;
  }

  public Gene(int x, int y) {
    this.x = x;
    this.y = y;
  }

  public double distanceTo(Gene other) {
    DecimalFormat f = new DecimalFormat("##.00");
    double distance = Math.sqrt(Math.pow(other.x - this.x, 2) + Math.pow(other.y - this.y, 2));
    return Double.parseDouble(f.format(distance));
  }
}
