package com.TravellingSalesmanProblem;

import java.util.*;

public class Population {

  public int genesCount, populationCount, sampleNumber;
  public Random random = new Random();
  public Gene[] genes;
  ArrayList<Individual> individuals;

  public Population(int genesCount, int sampleNumber) {
    this.genesCount = genesCount;
    this.populationCount = this.genesCount * 5;
    this.sampleNumber = sampleNumber;
    this.generateGenes();
    this.generateInitialPopulation();
  }

  public Individual fittest() {
    int fittestIndex = 0;
    for (int i = 0; i < this.populationCount; i++) {
      if (this.individuals.get(i).fitness < this.individuals.get(fittestIndex).fitness) fittestIndex = i;
    }

    return this.individuals.get(fittestIndex);
  }

  private void generateGenes() {
    this.genes = new Gene[this.genesCount];

    for(int i = 0; i < this.genesCount; i++) {
      int randomX = this.generateRandomNumber(100);
      int randomY = this.generateRandomNumber(100);
      this.genes[i] = new Gene(randomX, randomY);
    }
  }

  public int generateRandomNumber(int max) {
    return this.random.nextInt(max);
  }

  public void generateInitialPopulation() {
    this.individuals = new ArrayList<>();

    for(int i = 0; i < this.populationCount; i++) {
      Individual randomIndividual = this.generateIndividual();

      while(this.individuals.contains(randomIndividual)) {
        randomIndividual = this.generateIndividual();
      }

      this.individuals.add(randomIndividual);
    }
  }

  public Individual generateIndividual() {
    Gene[] chromosome = new Gene[this.genesCount];

    for(int i = 0; i < this.genesCount; i++) {
      int randomIndex = this.generateRandomNumber(this.genesCount);
      while(chromosome[randomIndex] != null) {
        randomIndex = this.generateRandomNumber(this.genesCount);
      }

      chromosome[randomIndex] = this.genes[i];
    }

    return new Individual(chromosome);
  }

  public Individual[] selectRandomIndividuals() {
    Individual[] randomIndividuals = new Individual[this.sampleNumber];

    for(int i = 0; i < this.sampleNumber; i++) {
      int randomIndex = this.generateRandomNumber(this.populationCount);
      while (Arrays.asList(randomIndividuals).contains(this.individuals.get(randomIndex))) {
        randomIndex = this.generateRandomNumber(this.populationCount);
      }

      randomIndividuals[i] = this.individuals.get(randomIndex);
    }

    return randomIndividuals;
  }

  public Individual[] getFittestParents() {
    Individual[] parents = new Individual[this.sampleNumber];
    PriorityQueue<Individual> pq = new PriorityQueue<>((first, second) -> {
      if (first.fitness < second.fitness) {
        return -1;
      } else if (first.fitness > second.fitness) {
        return 1;
      }

      return 0;
    });

    pq.addAll(this.individuals);

    for(int i = 0; i < this.sampleNumber; i++) {
      Individual mostFitParent = pq.poll();
      parents[i] = mostFitParent;
    }

    return parents;
  }

  public Individual[] getUnfitParents() {
    Individual[] parents = new Individual[this.sampleNumber];
    PriorityQueue<Individual> pq = new PriorityQueue<>((first, second) -> {
      if (first.fitness > second.fitness) {
        return -1;
      } else if (first.fitness < second.fitness) {
        return 1;
      }

      return 0;
    });

    pq.addAll(this.individuals);

    for(int i = 0; i < this.sampleNumber; i++) {
      Individual fittestParent = pq.poll();
      parents[i] = fittestParent;
    }

    return parents;
  }

  public Individual[] getRandomFittestParents() {
    Individual[] parents = new Individual[this.sampleNumber];

    for(int i = 0; i < this.sampleNumber; i++) {
      Individual fittestParent = this.findRandomFittestIndividual();

      while(Arrays.asList(parents).contains(fittestParent)) {
        fittestParent = this.findRandomFittestIndividual();
      }

      parents[i] = fittestParent;
    }

    return parents;
  }

  public Individual[] getRandomUnfitParents() {
    Individual[] parents = new Individual[this.sampleNumber];

    for(int i = 0; i < this.sampleNumber; i++) {
      Individual unfitParent = this.findRandomUnfitIndividual();

      while(Arrays.asList(parents).contains(unfitParent)) {
        unfitParent = this.findRandomUnfitIndividual();
      }

      parents[i] = unfitParent;
    }

    return parents;
  }

  private Individual findRandomUnfitIndividual() {
    Individual[] randomIndividuals = this.selectRandomIndividuals();
    Individual mostUnfit = randomIndividuals[0];

    for(int i = 1; i < this.sampleNumber; i++) {
      Individual currentIndividual = randomIndividuals[i];

      if (currentIndividual.fitness > mostUnfit.fitness) {
        mostUnfit = currentIndividual;
      }
    }

    return mostUnfit;
  }

  private Individual findRandomFittestIndividual() {
    Individual[] randomIndividuals = this.selectRandomIndividuals();
    Individual fittest = randomIndividuals[0];

    for(int i = 1; i < this.sampleNumber; i++) {
      Individual currentIndividual = randomIndividuals[i];

      if (currentIndividual.fitness < fittest.fitness) {
        fittest = currentIndividual;
      }
    }

    return fittest;
  }
}
