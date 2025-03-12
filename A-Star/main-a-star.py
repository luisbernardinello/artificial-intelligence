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

        # novo estado para baixo
        if posicao_vazia < 6:
            novo_tabuleiro = deepcopy(self.estado)
            self.troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia + 3)
            novo_estados.append(novo_tabuleiro)

        # novo estado para cima
        if posicao_vazia > 2:
            novo_tabuleiro = deepcopy(self.estado)
            self.troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia - 3)
            novo_estados.append(novo_tabuleiro)

        # novo estado para a direita
        if posicao_vazia % 3 < 2:
            novo_tabuleiro = deepcopy(self.estado)
            self.troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia + 1)
            novo_estados.append(novo_tabuleiro)

        # novo estado para a esquerda
        if posicao_vazia % 3 > 0:
            novo_tabuleiro = deepcopy(self.estado)
            self.troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia - 1)
            novo_estados.append(novo_tabuleiro)

        return [Tabuleiro(estado) for estado in novo_estados]

    @staticmethod
    def troca_elementos(lista, i, j):
        lista[i], lista[j] = lista[j], lista[i]

    def __eq__(self, outro):
        return self.estado == outro.estado

    def __hash__(self):
        return hash(tuple(self.estado))

    def imprime(self):
        for i in range(0, 9, 3):
            print(self.estado[i:i + 3])
        print()


class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent  # referência ao nó pai
        self.g = g  # custo do caminho até o nó
        self.h = h  # Heurística
        self.f = g + h  # f = g + h

    def __lt__(self, other):
        # nós com menor f são considerados melhores
        return self.f < other.f


# expande nós (gerar filhos)
def expand(node):
    """Gera os nós filhos a partir do estado atual"""
    filhos = node.state.gera_novos_estados()
    return [Node(state=filho, parent=node, g=node.g + 1, depth=node.depth + 1) for filho in filhos]


def heuristic_manhattan(state, goal):
    """Calcula a soma das distâncias de Manhattan para cada peça"""
    distancia_total = 0
    for i in range(len(state.estado)):
        if state.estado[i] != 0:
            posicao_atual = i
            posicao_objetivo = goal.estado.index(state.estado[i])
            distancia_total += abs(posicao_atual // 3 - posicao_objetivo // 3) + abs(posicao_atual % 3 - posicao_objetivo % 3)
    return distancia_total

def heuristic_naive(tabuleiro, objetivo):
    """
    Calcula o número de peças fora da posição correta.
    """
    contagem = 0
    for i in range(len(tabuleiro.estado)):
        if tabuleiro.estado[i] != objetivo.estado[i] and tabuleiro.estado[i] != 0:
            contagem += 1
    return contagem


# se o nó atual é a meta
def is_goal(state, goal):
    """Verifica se o estado atual é o objetivo"""
    return state == goal


def a_estrela(root, goal):
    """Implementação do algoritmo A*"""
    frontier = []
    heapq.heappush(frontier, root)  # fila de prioridade para nós baseados em f
    reached = {tuple(root.state.estado): root}  # dicionário para estados já alcançados
    nos_gerados = 0

    while frontier:
        # expande o melhor nó (com menor f-valor)
        current = heapq.heappop(frontier)

        # verifica se atingiu o objetivo
        if is_goal(current.state, goal):
            return reconstruct_path(current), nos_gerados

        # expande o nó e adicionar os filhos à fronteira
        for child in expand(current):
            child.h = heuristic_manhattan(child.state, goal)  # estima o custo restante
            child.f = child.g + child.h

            # se o estado ainda não foi alcançado, ou se esse caminho é melhor
            if tuple(child.state.estado) not in reached or child.f < reached[tuple(child.state.estado)].f:
                heapq.heappush(frontier, child)
                reached[tuple(child.state.estado)] = child
                nos_gerados += 1  # incrementa o contador de nós gerados

    # se não existir solução, retorna None
    return None, nos_gerados


def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]  # inverte o caminho


def imprime_solucao(caminho):
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

    escolha = int(input("Escolha o experimento a ser executado: \n1- Experimento 1 \n2- Experimento 2 \n "))

    if escolha == 1:
        estado_inicial = estado_inicial_1
        estado_objetivo = estado_objetivo_1
        print("Executando Experimento 1 com Heurística Manhattan...\n")
    elif escolha == 2:
        estado_inicial = estado_inicial_2
        estado_objetivo = estado_objetivo_2
        print("Executando Experimento 2 com Heurística Manhattan...\n")
    else:
        print("Escolha inválida!")
        return

    root = Node(state=estado_inicial, g=0, h=heuristic_manhattan(estado_inicial, estado_objetivo))
    
    tempo_inicial = time.time()
    
    caminho, nos_gerados = a_estrela(root, estado_objetivo)
    
    tempo_final = time.time()


    if caminho:
        imprime_solucao(caminho)
        print(f"Nós gerados: {nos_gerados}, Tempo: {tempo_final - tempo_inicial:.6f} segundos\n")
    else:
        print("Nenhuma solução encontrada.")


if __name__ == "__main__":
    main()
