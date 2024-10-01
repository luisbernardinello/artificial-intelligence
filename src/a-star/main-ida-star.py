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
        self.parent = parent  # Referência ao nó pai
        self.g = g  # Custo do caminho até o nó
        self.h = h  # Heurística
        self.f = g + h  # f = g + h

    def __lt__(self, other):
        return self.f < other.f


# Função para expandir nós (gerar filhos)
def expand(node):
    """Gera os nós filhos a partir do estado atual"""
    filhos = node.state.gera_novos_estados()
    return [Node(state=filho, parent=node, g=node.g + 1) for filho in filhos]


# Função heurística (Manhattan)
def heuristic(state, goal):
    """Calcula a soma das distâncias de Manhattan para cada peça"""
    distancia_total = 0
    for i in range(len(state.estado)):
        if state.estado[i] != 0:
            posicao_atual = i
            posicao_objetivo = goal.estado.index(state.estado[i])
            distancia_total += abs(posicao_atual // 3 - posicao_objetivo // 3) + abs(posicao_atual % 3 - posicao_objetivo % 3)
    return distancia_total


# Verificação se o nó atual é a meta
def is_goal(state, goal):
    """Verifica se o estado atual é o objetivo"""
    return state == goal


# Função principal do IDA*
def ida_star(root, goal):
    """Implementação do algoritmo IDA*"""
    def search(node, threshold):
        f = node.g + node.h

        # Se o valor de f exceder o limite atual, retornar esse valor
        if f > threshold:
            return f

        # Se for o objetivo, retornar o nó (sucesso)
        if is_goal(node.state, goal):
            return node

        min_threshold = math.inf  # Novo limite a ser definido

        # Expandir nós filhos
        for child in expand(node):
            child.h = heuristic(child.state, goal)
            result = search(child, threshold)

            # Se encontrou a solução, retorna o caminho
            if isinstance(result, Node):
                return result

            # Caso contrário, atualiza o novo limite
            if result < min_threshold:
                min_threshold = result

        return min_threshold

    # Iniciar com o nó raiz
    threshold = root.f

    while True:
        result = search(root, threshold)

        # Se encontrar a solução, retorna
        if isinstance(result, Node):
            return reconstruct_path(result)

        # Se não houver mais nós, retornar falha
        if result == math.inf:
            return None

        # Atualiza o threshold para a próxima iteração
        threshold = result


# Função para reconstruir o caminho a partir do nó solução
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]  # Inverte o caminho


# Função para imprimir a solução
def imprime_solucao(caminho):
    for estado in caminho:
        estado.imprime()
    print("Quantidade de passos:", len(caminho) - 1)


def main():
    estado_inicial = Tabuleiro([2, 8, 3, 1, 6, 4, 7, 0, 5])
    estado_objetivo = Tabuleiro([1, 2, 3, 8, 0, 4, 7, 6, 5])

    # Inicializar o nó raiz
    root = Node(state=estado_inicial, g=0, h=heuristic(estado_inicial, estado_objetivo))

    # Executar IDA*
    caminho = ida_star(root, estado_objetivo)

    if caminho:
        imprime_solucao(caminho)
    else:
        print("Nenhuma solução encontrada.")


if __name__ == "__main__":
    main()
