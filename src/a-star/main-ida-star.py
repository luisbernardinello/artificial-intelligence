import math
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
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


def expand(node):
    """Gera os nós filhos a partir do estado atual"""
    filhos = node.state.gera_novos_estados()
    return [Node(state=filho, parent=node, g=node.g + 1) for filho in filhos]


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


def ida_star(root, goal):
    """Implementação do algoritmo IDA*"""
    def search(node, threshold):
        f = node.g + node.h

        # caso do valor de f exceder o limite atual, retorna o valor
        if f > threshold:
            return f

        # caso seja o objetivo, retornar o nó (sucesso)
        if is_goal(node.state, goal):
            return node

        min_threshold = math.inf  # novo limite a ser definido

        # expande nós filhos
        for child in expand(node):
            child.h = heuristic(child.state, goal)
            result = search(child, threshold)

            # se encontrou a solução, retorna o resultado
            if isinstance(result, Node):
                return result

            # caso contrário, atualiza o novo limite
            if result < min_threshold:
                min_threshold = result

        return min_threshold

    # iniciar com o nó raiz
    threshold = root.f

    while True:
        result = search(root, threshold)

        # se encontrar a solução, retorna o caminho
        if isinstance(result, Node):
            return reconstruct_path(result)

        # se não existirem mais nós, retornar falha
        if result == math.inf:
            return None

        # atualiza o threshold para a prox iteração
        threshold = result


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


    root = Node(state=estado_inicial, g=0, h=heuristic(estado_inicial, estado_objetivo))

    caminho = ida_star(root, estado_objetivo)

    if caminho:
        imprime_solucao(caminho)
    else:
        print("Nenhuma solução encontrada.")


if __name__ == "__main__":
    main()
