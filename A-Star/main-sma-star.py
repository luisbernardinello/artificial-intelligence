import heapq
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
    def __init__(self, state, parent=None, g=0, h=0, depth=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
        self.depth = depth  # profundidade do nó na árvore de busca

    def __lt__(self, other):
        # nós com menor f são considerados melhores
        if self.f == other.f:
            return self.depth > other.depth  # em caso de empate, desempata pela profundidade
        return self.f < other.f


def expand(node):
    """Gera os nós filhos a partir do estado atual"""
    filhos = node.state.gera_novos_estados()
    return [Node(state=filho, parent=node, g=node.g + 1, depth=node.depth + 1) for filho in filhos]


def heuristic(state, goal):
    """Calcula a soma das distâncias de Manhattan para cada peça"""
    distancia_total = 0
    for i in range(len(state.estado)):
        if state.estado[i] != 0:
            posicao_atual = i
            posicao_objetivo = goal.estado.index(state.estado[i])
            distancia_total += abs(posicao_atual // 3 - posicao_objetivo // 3) + abs(posicao_atual % 3 - posicao_objetivo % 3)
    return distancia_total


def is_goal(state, goal):
    """Verifica se o estado atual é o objetivo"""
    return state == goal


def sma_star(root, goal, memory_limit):
    """algoritmo SMA*"""
    frontier = []
    heapq.heappush(frontier, root)  # fila de prioridade para nós baseados em f
    reached = {tuple(root.state.estado): root}  # dicionário para estados já alcançados

    while frontier:
        # se a memória está cheia, remove o pior nó (com maior f-valor)
        if len(frontier) > memory_limit:
            worst_node = max(frontier, key=lambda n: n.f)  # encontra o pior nó
            frontier.remove(worst_node)  # remove manualmente da fronteira
            heapq.heapify(frontier)  # reajuste da heap após a remoção
            # atualizar o nó pai com o valor de f do nó removido
            if worst_node.parent:
                worst_node.parent.f = max(worst_node.parent.f, worst_node.f)
            continue

        # expande o melhor nó (com menor f-valor)
        current = heapq.heappop(frontier)

        # se atingiu o objetivo retorna o caminho
        if is_goal(current.state, goal):
            return reconstruct_path(current)

        # expande o nó e adicionar os filhos à fronteira
        for child in expand(current):
            child.h = heuristic(child.state, goal)  # estima o custo restante
            child.f = child.g + child.h

            # se o estado ainda não foi alcançado, ou se esse caminho é melhor
            if tuple(child.state.estado) not in reached or child.f < reached[tuple(child.state.estado)].f:
                heapq.heappush(frontier, child)
                reached[tuple(child.state.estado)] = child

    # se a memória estiver cheia e não existir solução possível, retorna falha
    return None


def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]


def imprime_solucao(caminho):
    for estado in caminho:
        estado.imprime()
    print("Quantidade de passos:", len(caminho) - 1)


def main():
    estado_inicial = Tabuleiro([2, 8, 3, 1, 6, 4, 7, 0, 5])
    estado_objetivo = Tabuleiro([1, 2, 3, 8, 0, 4, 7, 6, 5])

    root = Node(state=estado_inicial, g=0, h=heuristic(estado_inicial, estado_objetivo), depth=0)

    # limite de memória (número de nós na fronteira)
    memory_limit = 1000

    caminho = sma_star(root, estado_objetivo, memory_limit)

    if caminho:
        imprime_solucao(caminho)
    else:
        print("Nenhuma solução encontrada.")


if __name__ == "__main__":
    main()
