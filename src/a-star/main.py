import heapq
import time
from copy import deepcopy

class Tabuleiro:
    def __init__(self, estado):
        self.estado = estado

    def gera_novos_estados(self):
        """
        Gera todos os novos estados possíveis para o espaço vazio (0) do tabuleiro.
        """
        novo_estados = []
        posicao_vazia = self.estado.index(0)

        # Novo estado para baixo
        if posicao_vazia < 6:
            novo_tabuleiro = deepcopy(self.estado)
            self.troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia + 3)
            novo_estados.append(novo_tabuleiro)

        # Novo estado para cima
        if posicao_vazia > 2:
            novo_tabuleiro = deepcopy(self.estado)
            self.troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia - 3)
            novo_estados.append(novo_tabuleiro)

        # Novo estado para a direita
        if posicao_vazia % 3 < 2:
            novo_tabuleiro = deepcopy(self.estado)
            self.troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia + 1)
            novo_estados.append(novo_tabuleiro)

        # Novo estado para a esquerda
        if posicao_vazia % 3 > 0:
            novo_tabuleiro = deepcopy(self.estado)
            self.troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia - 1)
            novo_estados.append(novo_tabuleiro)

        return [Tabuleiro(estado) for estado in novo_estados]

    @staticmethod
    def troca_elementos(lista, i, j):
        """
        Troca os elementos na posição i e j da lista dos tabuleiros.
        """
        lista[i], lista[j] = lista[j], lista[i]

    def __eq__(self, outro): #equals
        return self.estado == outro.estado

    def __hash__(self): #hash que identifica o objeto em estruturas como set e dict
        return hash(tuple(self.estado)) #permite calcular um valor de hash para cada estado

    def imprime(self):
        """
        Imprime o tabuleiro em uma forma 3x3.
        """
        for i in range(0, 9, 3):
            print(self.estado[i:i + 3])
        print()

class Node:
    def __init__(self, tabuleiro, g, caminho):
        self.tabuleiro = tabuleiro
        self.g = g  # Custo acumulado
        self.caminho = caminho  # Caminho até o estado atual
        self.f = 0  # Avaliação de custo f(n) = g(n) + h(n)

    def __lt__(self, outro): #less than
        return self.f < outro.f

def h_naive(tabuleiro, objetivo):
    """
    Calcula o número de peças fora da posição correta.
    """
    contagem = 0
    for i in range(len(tabuleiro.estado)):
        if tabuleiro.estado[i] != objetivo.estado[i] and tabuleiro.estado[i] != 0:
            contagem += 1
    return contagem

def h_manhattan(tabuleiro, objetivo):
    """
    Calcula a soma das distâncias de Manhattan para cada peça.
    """
    distancia_total = 0
    for i in range(len(tabuleiro.estado)):
        if tabuleiro.estado[i] != 0:
            posicao_atual = i
            posicao_objetivo = objetivo.estado.index(tabuleiro.estado[i])
            distancia_total += abs(posicao_atual // 3 - posicao_objetivo // 3) + abs(posicao_atual % 3 - posicao_objetivo % 3)
    return distancia_total

def a_estrela(inicial, objetivo, heuristica):
    """
    Aplica o algoritmo A* para resolver o quebra-cabeça.
    """
    abertos = []
    heapq.heappush(abertos, Node(inicial, 0, []))  # Inicializa com o estado inicial
    fechados = set()

    while abertos:
        node_atual = heapq.heappop(abertos)

        if node_atual.tabuleiro == objetivo:  # Se o estado atual for o objetivo, retorna o caminho
            return node_atual.caminho + [node_atual.tabuleiro], len(fechados), node_atual.g

        if node_atual.tabuleiro in fechados:
            continue

        fechados.add(node_atual.tabuleiro)

        for novo_tabuleiro in node_atual.tabuleiro.gera_novos_estados():
            if novo_tabuleiro not in fechados:
                novo_caminho = node_atual.caminho + [node_atual.tabuleiro]
                novo_g = node_atual.g + 1
                novo_node = Node(novo_tabuleiro, novo_g, novo_caminho)
                novo_node.f = novo_g + heuristica(novo_tabuleiro, objetivo)
                heapq.heappush(abertos, novo_node)

    return None, len(fechados)

def imprime_solucao(caminho):
    """
    Imprime os passos da solução.
    """
    for estado in caminho:
        estado.imprime()
    print("Quantidade de passos:", len(caminho) - 1)

def main():
    estado_inicial_1 = Tabuleiro([2, 8, 3,
                                  1, 6, 4,
                                  7, 0, 5])

    estado_objetivo_1 = Tabuleiro([1, 2, 3,
                                   8, 0, 4,
                                   7, 6, 5])

    estado_inicial_2 = Tabuleiro([7, 2, 4,
                                  5, 0, 6,
                                  8, 3, 1])

    estado_objetivo_2 = Tabuleiro([1, 2, 3,
                                   4, 5, 6,
                                   7, 8, 0])

    escolha = int(input("Escolha o experimento a ser executado: \n1- Experimento 1\n2- Experimento 2\n "))

    if escolha == 1:
        estado_inicial = estado_inicial_1
        estado_objetivo = estado_objetivo_1
    elif escolha == 2:
        estado_inicial = estado_inicial_2
        estado_objetivo = estado_objetivo_2
    else:
        print("Escolha inválida!")
        return

    print("------------------------------------------")
    
    # Heurística naive
    tempo_inicial = time.time()
    solucao, nos_gerados_h1, g_h1 = a_estrela(estado_inicial, estado_objetivo, h_naive)
    tempo_final = time.time()
    
    if solucao:
        print("Heurística Naive:")
        imprime_solucao(solucao)
        print(f"Nós gerados: {nos_gerados_h1}, Tempo: {tempo_final - tempo_inicial:.6f} segundos\n")
    else:
        print("Nenhuma solução foi encontrada.")

    print("------------------------------------------")

    # Heurística Manhattan
    tempo_inicial = time.time()
    solucao, nos_gerados_h2, g_h2 = a_estrela(estado_inicial, estado_objetivo, h_manhattan)
    tempo_final = time.time()

    if solucao:
        print("Heurística Manhattan:")
        imprime_solucao(solucao)
        print(f"Nós gerados: {nos_gerados_h2}, Tempo: {tempo_final - tempo_inicial:.6f} segundos\n")
    else:
        print("Nenhuma solução foi encontrada.")

if __name__ == "__main__":
    main()
