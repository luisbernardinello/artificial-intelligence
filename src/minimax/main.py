import math 
from copy import deepcopy

class Node:
    def __init__(self, tabuleiro, movimento = None, node_pai = None):
        self.tabuleiro = tabuleiro
        self.movimento = movimento
        self.node_pai = node_pai
        self.nodes_filhos = []
        self.valor = None
        
def minimax(tabuleiro, maximizando):
    raiz = Node(tabuleiro)
    nodes_inexplorados = [raiz] # nodes da arvore que ainda precisam ser analisados.
    nodes_expandidos = 0

    while nodes_inexplorados:
        node = nodes_inexplorados.pop() # ultimo node da arvore que sera analisado
        nodes_expandidos += 1

        if folha(node.tabuleiro): # estado final
            node.valor = avalia_tabuleiro(node.tabuleiro) 
        else: # se nao for node folha verifica de quem eh a vez, gera os movimentos validos
            turno = jogador(node.tabuleiro)
            movimentos_validos = movimentos_possiveis(node.tabuleiro)

            for movimento in movimentos_validos: # para cada movimento valido gera um novo estado do tabuleiro e cria um novo node filho que sera analisado
                novo_tabuleiro = gera_movimento(node.tabuleiro, movimento, turno)
                node_pai = node
                node_filho = Node(novo_tabuleiro, movimento, node_pai)
                node.nodes_filhos.append(node_filho)
                nodes_inexplorados.append(node_filho)

    melhor_valor = retorna_melhor_valor(raiz, maximizando)

    for filho in raiz.nodes_filhos: # verifico nodes filhos
        if filho.valor == melhor_valor: # se for o melhor armazeno o estado do tabuleiro que sera retornado
            tabuleiro_final = filho.tabuleiro
            break

    return tabuleiro_final, nodes_expandidos

def retorna_melhor_valor(node, maximizando):
    if node.valor is not None: # se o valor ja foi calculado retorna o valor
        return node.valor

    if maximizando:
        valor_max = -math.inf # se estiver maximizando inicia com o pior valor possivel para entrar na recursao
        for filho in node.nodes_filhos: # para cada filho calcula o valor do filho
            valor = retorna_melhor_valor(filho, False)
            valor_max = max(valor_max, valor) # pega o maior valor e retorna
        node.valor = valor_max

    else:
        valor_min = math.inf # analogo ao maximizando
        for filho in node.nodes_filhos:
            valor = retorna_melhor_valor(filho, True)
            valor_min = min(valor_min, valor)
        node.valor = valor_min

    return node.valor

def folha(tabuleiro): # tabuleiro no estado final
    if avalia_tabuleiro(tabuleiro) != 0:
        return True
    elif movimentos_possiveis(tabuleiro) == 0: #lista vazia
        return True
    
    return 0
    
def avalia_tabuleiro(tabuleiro):
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] != "_":
            if tabuleiro[i][0] == "X":
                return 1
            else: return -1
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] != "_":
            if tabuleiro[i][0] == "X":
                return 1
            else: return -1
    #diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != "_": 
        if tabuleiro[i][0] == "X":
                return 1
        else: return -1
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != "_": 
        if tabuleiro[i][0] == "X":
                return 1
        else: return -1
    return 0

def movimentos_possiveis(tabuleiro):
    movimentos = [] 
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == "_":
                movimentos.append((i, j))
                
    return movimentos

def jogador(tabuleiro):
    conta_x = 0
    conta_o = 0
    for linha in tabuleiro: # conta e retorna o jogador com base na quantia de X que tem no tabuleiro, se tiver menos X do que O, vez do X
        conta_x += linha.count("X")
        conta_o += linha.count("O")
        
    return "X" if conta_x <= conta_o else "O"

def gera_movimento(tabuleiro, movimento, turno):
    novo_tabuleiro = deepcopy(tabuleiro) # deepcopy pois o tabuleiro se trata de uma lista de listas (matriz)
    novo_tabuleiro[movimento[0]][movimento[1]] = turno # marca o simbolo do jogador (turno = "X" ou "O") na posicao correspondente que veio pelo parametro
    
    return novo_tabuleiro

def imprime_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" | ".join(linha))
        print("-" * 9)

def main():

    jogo_1 = [["X", "O", "X"],
              ["O", "X", "O"],
              ["_", "_", "_"]]

    jogo_2 = [["X", "O", "X"],
              ["O", "O", "X"],
              ["_", "_", "_"]]

    jogo_3 = [["O", "_", "X"],
              ["_", "X", "_"],
              ["O", "_", "_"]]

    
    for i, tabuleiro_inicial in enumerate([jogo_1, jogo_2, jogo_3], start=1):
        print(f"Experimento {i}:\n")
        print("Estado inicial:")
        imprime_tabuleiro(tabuleiro_inicial)

        tabuleiro_final, nodes_expandidos = minimax(tabuleiro_inicial, True)
        print("Estado final depois de executar o Minimax:")
        imprime_tabuleiro(tabuleiro_final)
        print(f"Nodes expandidos: {nodes_expandidos}")

        print("------------------------------------------")

if __name__ == "__main__":
    main()

