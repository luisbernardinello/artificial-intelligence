import random
import matplotlib.pyplot as plt
import numpy as np

class Individuo:
    def __init__(self, gene, fitness=None):
        self.gene = gene
        self.fitness = fitness

    def calcula_fitness(self):
        """ calculo do fitness sendo a diferença entre os dois subconjuntos """
        soma_A = 0
        soma_B = 0
        
        for i in range(len(self.gene)): # soma de cada subconjunto
            if self.gene[i] == 0:
                soma_A += valores[i]
            else:
                soma_B += valores[i]
        
        # atribui ao fitness a diferença entre as somas
        self.fitness = abs(soma_A - soma_B)


    def mutar(self, taxa_mutacao):
        """calcula a mutação invertendo os genes com base na taxa de mutação fornecida """
        for i in range(len(self.gene)):
            if random.random() < taxa_mutacao:
                self.gene[i] = 1 - self.gene[i]  # inversão dos genes, 0 para 1 e 1 para 0


class Population:
    def __init__(self, size, num_genes):
        self.size = size
        self.num_genes = num_genes
        
        individuos = []
        for _ in range(size):
            gene = [random.randint(0, 1) for _ in range(num_genes)]
            individuo = Individuo(gene)
            #individuo.calcula_fitness()   
            individuos.append(individuo)
        self.individuos = individuos
        

    def melhor_individuo(self):
        """ calcula o menor fitness (melhor individuo da população)"""
        melhor = self.individuos[0]  # melhor será o primeiro no inicio
        
        # encontra o individuo de menor fitness
        for individuo in self.individuos:
            if individuo.fitness < melhor.fitness:
                melhor = individuo
        
        return melhor
    
    def avaliar_populacao(self):
        for individuo in self.individuos:
            individuo.calcula_fitness()

    def selecao_torneio(self, k=3):
        """ seleção feita por torneio """
        torneio = random.sample(self.individuos, k)  # k individuos aleatoriamente por torneio
        melhor = torneio[0]  # melhor será o primeiro no inicio
        
        # na população reduzida do torneio, encontra o menor fitness
        for individuo in torneio:
            if individuo.fitness < melhor.fitness:
                melhor = individuo
        
        return melhor



def crossover(pai1, pai2):
    """ faz o crossover entre dois indivíduos da população """
    ponto_corte = random.randint(1, len(pai1.gene) - 1) # ponto de corte gerado aleatoriamente
    filho_genes = pai1.gene[:ponto_corte] + pai2.gene[ponto_corte:] # pega os genes do pai 1 do inicio até o ponto de corte e do pai 2 do ponto de corte até o fim
    return Individuo(filho_genes) # novo individuo gerado com os novos genes


def algoritmo_genetico(popsize, num_geracoes, taxa_crossover, taxa_mutacao):
    populacao = Population(popsize, len(valores)) # inicializa a população
    populacao.avaliar_populacao()

    melhor_fitness_geracao = []
    fitness_medio_geracao = []

    for geracao in range(num_geracoes):
        nova_populacao = []

        while len(nova_populacao) < popsize:
            # pega exemplares da população pelo torneio
            pai1 = populacao.selecao_torneio()
            pai2 = populacao.selecao_torneio()

            # faz o crossover
            if random.random() < taxa_crossover:
                filho = crossover(pai1, pai2)
            else:
                filho = random.choice([pai1, pai2])

            # insere mutação
            filho.mutar(taxa_mutacao)

            # calcula o fitness do novo filho
            filho.calcula_fitness()
            
            nova_populacao.append(filho)

        populacao.individuos = nova_populacao

        # avaliação do melhor individuo e do fitness médio da população
        melhor_individuo = populacao.melhor_individuo()
        fitness_medio = sum([ind.fitness for ind in populacao.individuos]) / popsize

        melhor_fitness_geracao.append(melhor_individuo.fitness)
        fitness_medio_geracao.append(fitness_medio)

        print(f'Geração {geracao+1} | Melhor Fitness: {melhor_individuo.fitness} | Fitness Médio: {fitness_medio}')

    # gera o gráfico da população.
    plt.plot(melhor_fitness_geracao, label='Melhor Fitness')
    plt.plot(fitness_medio_geracao, label='Fitness Médio')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.title('Convergência do Algoritmo Genético')
    plt.legend()
    plt.show()

    return populacao.melhor_individuo()


def main():
    dimensao = 30 # dimensao do problema (numero de genes)
    global valores
    
    valores = np.random.randint(0, 10, dimensao)

    # global valores
    # valores = [
    #     15, 30, 25, 18, 12, 9, 22, 33, 41, 5, 16, 27, 13, 19, 24, 
    #     11, 29, 36, 23, 42, 17, 39, 6, 21, 31, 14, 28, 10, 35, 20
    # ]

    popsize = 50
    num_geracoes = 150
    taxa_crossover = 0.9
    taxa_mutacao = 0.02


    melhor_solucao = algoritmo_genetico(popsize, num_geracoes, taxa_crossover, taxa_mutacao)
    print(f'Melhor solução: {melhor_solucao.gene}, Fitness: {melhor_solucao.fitness}')


if __name__ == "__main__":
    main()
