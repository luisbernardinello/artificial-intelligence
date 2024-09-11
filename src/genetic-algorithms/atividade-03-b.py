import os
import numpy as np
import random
import matplotlib.pyplot as plt

uk_dist_arq = os.path.join("atividade-03-b/uk12/uk12_dist.txt")
uk_cities_arq = os.path.join("atividade-03-b/uk12/uk12_name.txt")

ha30_dist_arq = os.path.join("atividade-03-b/ha30/ha30_dist.txt")
ha30_cities_arq = os.path.join("atividade-03-b/ha30/ha30_name.txt")



def carrega_matriz_dist(filename):
    with open(filename, 'r') as f:
        matriz_dist = []
        for linha in f:
            matriz_dist.append(list(map(int, linha.split())))
    return np.array(matriz_dist)


def carrega_nomes_cidades(filename):
    with open(filename, 'r') as f:
        cidades = [linha.strip() for linha in f]
    return cidades


class Individuo:
    def __init__(self, gene):
        self.gene = gene
        self.fitness = None

    def calcula_fitness(self, matriz_dist):
        """ Cálculo da distância total (fitness) da rota """
        self.fitness = calcula_distancia(self.gene, matriz_dist)

    def mutar(self, taxa_mutacao):
        """ Aplica mutação (swap) com base na taxa de mutação """
        if random.random() < taxa_mutacao:
            i, j = random.sample(range(1, len(self.gene)), 2)  # evita a cidade de origem
            self.gene[i], self.gene[j] = self.gene[j], self.gene[i]

class Population:
    def __init__(self, size, num_cities):
        self.size = size
        self.num_cities = num_cities
        
        self.individuos = []
        for _ in range(size):
            # Criação direta dos genes (rota aleatória)
            gene = list(range(1, num_cities))  # Evita a cidade de origem
            random.shuffle(gene)
            gene = [0] + gene  # Adiciona a cidade de origem no início

            # Criação do indivíduo com os genes gerados
            individuo = Individuo(gene)
            self.individuos.append(individuo)
            
            
    def avaliar_populacao(self, matriz_dist):
        for individuo in self.individuos:
            individuo.calcula_fitness(matriz_dist)

    def melhor_individuo(self):
        melhor = self.individuos[0]  # melhor será o primeiro no inicio
        
        # encontra o individuo de menor fitness
        for individuo in self.individuos:
            if individuo.fitness < melhor.fitness:
                melhor = individuo
        
        return melhor

    def selecao_torneio(self, k=3):
        """ Seleção por torneio """
        torneio = random.sample(self.individuos, k)
        melhor = torneio[0]
                # na população reduzida do torneio, encontra o menor fitness
        for individuo in torneio:
            if individuo.fitness < melhor.fitness:
                melhor = individuo
        
        return melhor

        


def calcula_distancia(route, matriz_dist):
    """ Soma das distâncias da rota """
    distancia_total = sum(matriz_dist[route[i], route[i + 1]] for i in range(len(route) - 1))
    distancia_total += matriz_dist[route[-1], route[0]]  # Volta à origem
    return distancia_total

def pmx_crossover(pai1, pai2):
    """ Implementação do crossover PMX """
    size = len(pai1.gene)
    filho1, filho2 = pai1.gene[:], pai2.gene[:]

    # Pontos de crossover
    cx1, cx2 = sorted(random.sample(range(1, size), 2))

    # Troca de segmentos entre os pais
    for i in range(cx1, cx2):
        temp1, temp2 = filho1[i], filho2[i]
        filho1[i], filho2[i] = temp2, temp1
    return Individuo(filho1), Individuo(filho2)

def algoritmo_genetico(matriz_dist, popsize, num_geracoes, taxa_crossover, taxa_mutacao):
    populacao = Population(popsize, len(matriz_dist))
    populacao.avaliar_populacao(matriz_dist)
    
    melhor_fitness_geracao = []
    fitness_medio_geracao = []

    for geracao in range(num_geracoes):
        nova_populacao = []

        while len(nova_populacao) < popsize:
            pai1 = populacao.selecao_torneio()
            pai2 = populacao.selecao_torneio()

            if random.random() < taxa_crossover:
                filho1, filho2 = pmx_crossover(pai1, pai2)
            else:
                filho1, filho2 = pai1, pai2

            filho1.mutar(taxa_mutacao)
            filho2.mutar(taxa_mutacao)

            filho1.calcula_fitness(matriz_dist)
            filho2.calcula_fitness(matriz_dist)

            nova_populacao.extend([filho1, filho2])

        populacao.individuos = nova_populacao[:popsize]

        # Avaliação da geração
        melhor_individuo = populacao.melhor_individuo()
        fitness_medio = sum([ind.fitness for ind in populacao.individuos]) / popsize

        melhor_fitness_geracao.append(melhor_individuo.fitness)
        fitness_medio_geracao.append(fitness_medio)

        print(f'Geração {geracao+1} | Melhor Fitness: {melhor_individuo.fitness} | Fitness Médio: {fitness_medio:.2f}')

    plt.plot(melhor_fitness_geracao, label='Melhor Fitness')
    plt.plot(fitness_medio_geracao, label='Fitness Médio')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.title('Convergência do Algoritmo Genético (TSP)')
    plt.legend()
    plt.show()

    return populacao.melhor_individuo()

def main():

    popsize = 50
    num_geracoes = 250
    taxa_crossover = 0.9
    taxa_mutacao = 0.02    
    
    uk12_dist = carrega_matriz_dist(uk_dist_arq)
    uk12_cities = carrega_nomes_cidades(uk_cities_arq)
    
    ha30_dist = carrega_matriz_dist(ha30_dist_arq)
    ha30_cities = carrega_nomes_cidades(ha30_cities_arq)


    # experimento com uk12
    print("Experimento com uk12")

    melhor_solucao = algoritmo_genetico(uk12_dist, popsize, num_geracoes, taxa_crossover, taxa_mutacao)
    melhor_rota = [uk12_cities[i] for i in melhor_solucao.gene]
    melhor_distancia = melhor_solucao.fitness

    print(f'Melhor rota: {melhor_rota}')
    print(f'Distância total: {melhor_distancia}')
    
    
    # experimento com ha30
    print("------------------------------------------\n")
    
    print("Experimento com ha30")
    melhor_solucao_2 = algoritmo_genetico(ha30_dist, popsize, num_geracoes, taxa_crossover, taxa_mutacao)
    melhor_rota_2 = [ha30_cities[i] for i in melhor_solucao_2.gene]
    melhor_distancia_2 = melhor_solucao_2.fitness
    
    print(f'Melhor rota: {melhor_rota_2}')
    print(f'Distância total: {melhor_distancia_2}')
    

if __name__ == "__main__":
    main()
