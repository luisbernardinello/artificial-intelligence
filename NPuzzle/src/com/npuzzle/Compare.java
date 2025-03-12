package com.npuzzle;

import java.util.Comparator;

public class Compare implements Comparator<Node> {
    @Override
    public int compare(Node first, Node second) {
      if (first.f() < second.f()) {
        return -1;
      } else if (first.f() > second.f()) {
        return 1;
      }

      return 0;
    }
}
