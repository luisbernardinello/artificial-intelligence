package com.TravellingSalesmanProblem;

public class Individual {

  public int genesCount;
  public Gene[] chromosome;
  public double fitness;

  public Individual(int genesCount) {
    this.genesCount = genesCount;
    this.chromosome = new Gene[this.genesCount];
  }

  public Individual(Gene[] genes) {
    this.chromosome = genes;
    this.genesCount = genes.length;
    this.setFitness();
  }

  public void setFitness() {
    for(int i = 0; i < this.genesCount - 1; i++) {
      this.fitness += this.chromosome[i].distanceTo(this.chromosome[i + 1]);
    }
  }

  public void swapGenes(int firstGeneIndex, int secondGeneIndex) {
    Gene gene = this.chromosome[firstGeneIndex];
    this.chromosome[firstGeneIndex] = this.chromosome[secondGeneIndex];
    this.chromosome[secondGeneIndex] = gene;
  }
}
