package com.TravellingSalesmanProblem;

import java.util.*;

public class Solver {
  public int genesCount, sampleNumber;
  public Random random = new Random();
  Population population;

  public Solver(int n) {
    this.genesCount = n;
    this.sampleNumber = n/2;
    if (this.sampleNumber % 2 != 0) {
      this.sampleNumber--;
    }

    this.population = new Population(n, sampleNumber);
  }

  public void start() {
    int generation = 0;
    int maxGenerations = this.genesCount * 10;
    int sameBestFitnessCount = 0;
    boolean randomSearch = false;
    ArrayList<Integer> generationsToPrint = this.pickGenerationsToPrint(maxGenerations);

    while(generation < maxGenerations) {
      generation++;
      Individual fittestBeforeSearch = this.population.fittest();

      if (generation == 10 || generationsToPrint.contains(generation)) {
        this.printGenerationFittest(generation);
      }

      search(randomSearch);

      Individual fittestAfterSearch = this.population.fittest();
      if (fittestBeforeSearch.fitness == fittestAfterSearch.fitness) {
        sameBestFitnessCount++;
      } else {
        sameBestFitnessCount = 0;
      }

      if (sameBestFitnessCount > 10) {
        randomSearch = true;
        this.randomMutate();
      } else {
        randomSearch = false;
      }
    }

    this.printGenerationFittest(generation);
  }

  public void randomMutate() {
    for(int i = 0; i < Math.sqrt(this.genesCount); i++) {
      int randomIndex = this.generateRandomNumber(this.population.populationCount);
      this.population.individuals.set(randomIndex, this.mutate(this.population.individuals.get(randomIndex)));
    }
  }

  public void printGenerationFittest(int generation) {
    System.out.println("Generation " + generation + " fittest: " + this.population.fittest().fitness);
  }

  public ArrayList<Integer> pickGenerationsToPrint(int maxGenerations) {
    ArrayList<Integer> generationsToPrint = new ArrayList<>();

    for(int i = 0; i < 3; i++) {
      int randomNumber = this.generateRandomNumber(maxGenerations - 1);
      while (randomNumber <= 10) {
        randomNumber = this.generateRandomNumber(maxGenerations - 1);
      }

      generationsToPrint.add(randomNumber);
    }

    return generationsToPrint;
  }

  public void search(boolean randomSearch) {
    Individual[] parents;
    if(randomSearch) {
      parents = this.population.getRandomFittestParents();
    } else {
      parents = this.population.getFittestParents();
    }

    Individual[] children = new Individual[this.sampleNumber];
    int mutateCounter = 0;

    for(int i = 0; i < this.sampleNumber - 1; i+=2) {
      Individual[] crossoverChildren = this.crossover(parents[i], parents[i + 1]);

      if (mutateCounter == 0) {
        crossoverChildren[0] = this.mutate(crossoverChildren[0]);
        crossoverChildren[1] = this.mutate(crossoverChildren[1]);
      }

      crossoverChildren[0].setFitness();
      crossoverChildren[1].setFitness();

      children[i] = crossoverChildren[0];
      children[i + 1] = crossoverChildren[1];
      mutateCounter++;
      if (mutateCounter == 3) mutateCounter = 0;
    }

    this.survivorSelection(children, randomSearch);
  }

  public void survivorSelection(Individual[] children, boolean randomSearch) {
    Individual[] unfitParents;

    if (randomSearch) {
      unfitParents = this.population.getRandomUnfitParents();
    } else {
      unfitParents = this.population.getUnfitParents();
    }

    for(int i = 0; i < this.sampleNumber; i++) {
      int parentIndex = this.population.individuals.indexOf(unfitParents[i]);
      this.population.individuals.set(parentIndex, children[i]);
    }
  }

  public Individual mutate(Individual individual) {
    int firstGeneIndex = this.generateRandomNumber(this.genesCount);
    int secondGeneIndex = this.generateRandomNumber(this.genesCount);

    while(secondGeneIndex == firstGeneIndex) {
      secondGeneIndex = this.generateRandomNumber(this.genesCount);
    }

    individual.swapGenes(firstGeneIndex, secondGeneIndex);

    return individual;
  }

  public Individual[] crossover(Individual firstParent, Individual secondParent) {
    Individual firstChild = new Individual(this.genesCount);
    Individual secondChild = new Individual(this.genesCount);

    int[] crossoverPoints = this.getCrossoverPoints();

    int firstCrossoverPoint = Math.min(crossoverPoints[0], crossoverPoints[1]);
    int secondCrossoverPoint = Math.max(crossoverPoints[0], crossoverPoints[1]);

    for(int i = firstCrossoverPoint; i <= secondCrossoverPoint; i++) {
      firstChild.chromosome[i] = secondParent.chromosome[i];
      secondChild.chromosome[i] = firstParent.chromosome[i];
    }

    firstChild = this.setChild(firstChild, secondParent, secondCrossoverPoint);
    secondChild = this.setChild(secondChild, firstParent, secondCrossoverPoint);

    return new Individual[] { firstChild, secondChild };
  }

  public int[] getCrossoverPoints() {
    int firstRandomPoint = this.generateRandomNumber(this.genesCount);
    while(firstRandomPoint == 0 || firstRandomPoint == this.genesCount - 1) {
      firstRandomPoint = this.generateRandomNumber(this.genesCount);
    }

    int secondRandomPoint = this.generateRandomNumber(this.genesCount);
    while(secondRandomPoint == 0 || secondRandomPoint == this.genesCount - 1 || secondRandomPoint == firstRandomPoint) {
      secondRandomPoint = this.generateRandomNumber(this.genesCount);
    }

    return new int[] { firstRandomPoint, secondRandomPoint };
  }

  public Individual setChild(Individual child, Individual parent, int secondCrossoverPoint) {
    int parentIndex = secondCrossoverPoint + 1;
    int childIndex = secondCrossoverPoint + 1;

    while(parentIndex != secondCrossoverPoint) {
      if (childIndex == this.genesCount) childIndex = 0;
      if (parentIndex == this.genesCount) parentIndex = 0;

      Gene gene = parent.chromosome[parentIndex];
      if (Arrays.asList(child.chromosome).contains(gene)) {
        parentIndex = this.updateIndex(parentIndex);
        continue;
      }

      child.chromosome[childIndex] = parent.chromosome[parentIndex];
      parentIndex = this.updateIndex(parentIndex);
      childIndex = this.updateIndex(childIndex);
    }

    return child;
  }

  public int updateIndex(int index) {
    index++;
    if (index >= this.genesCount) {
      index = 0;
    }

    return index;
  }

  private int generateRandomNumber(int max) {
    return this.random.nextInt(max);
  }
}
