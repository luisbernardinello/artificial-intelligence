import heapq
import time

def troca_elementos(lista, i, j):
    """
    Troca os elementos na posição i e j da lista dos tabuleiros.
    """
    lista[i], lista[j] = lista[j], lista[i]

def gera_novos_estados(tabuleiro):
    """
    Gera todos os novo_estados possíveis para o espaço vazio do jogo (o 0 do tabuleiro).
    """
    novo_estados = []
    posicao_vazia = tabuleiro.index(0)

    # novo_estado para baixo
    if posicao_vazia < 6:  # espaço vazio não está na última linha
        novo_tabuleiro = tabuleiro[:]
        troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia + 3)
        novo_estados.append(novo_tabuleiro)

    # novo_estado para cima
    if posicao_vazia > 2:  # espaço vazio não está na primeira linha
        novo_tabuleiro = tabuleiro[:]
        troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia - 3)
        novo_estados.append(novo_tabuleiro)

    # novo_estado para a direita
    if posicao_vazia % 3 < 2:  # espaço vazio não está na última coluna (índice 2, 5, 8)
        novo_tabuleiro = tabuleiro[:]
        troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia + 1)
        novo_estados.append(novo_tabuleiro)

    # novo_estado para a esquerda
    if posicao_vazia % 3 > 0:  # espaço vazio não está na primeira coluna (índice 0, 3, 6)
        novo_tabuleiro = tabuleiro[:]
        troca_elementos(novo_tabuleiro, posicao_vazia, posicao_vazia - 1)
        novo_estados.append(novo_tabuleiro)

    return novo_estados


def h_naive(tabuleiro, objetivo):
    """
    Calcula o numero de peças que estão fora da posição correta de forma simples,
    excluindo o espaço vazio do jogo (valor 0 no tabuleiro).
    """
    contagem = 0
    for i in range(len(tabuleiro)):
        if tabuleiro[i] != objetivo[i] and tabuleiro[i] != 0:
            contagem += 1
    return contagem


def h_manhattan(tabuleiro, objetivo):
    """
    Calcula a soma das distâncias de Manhattan para cada peça,
    excluindo o espaço vazio do jogo (valor 0 no tabuleiro).
    """
    distancia_total = 0
    for i in range(len(tabuleiro)):
        if tabuleiro[i] != 0:
            posicao_atual = i
            posicao_objetivo = objetivo.index(tabuleiro[i])
            distancia_total += abs(posicao_atual // 3 - posicao_objetivo // 3) + abs(posicao_atual % 3 - posicao_objetivo % 3) #  // temos o numero da linha e % temos o numero da coluna
    return distancia_total


def a_estrela(inicial, objetivo, heuristica):
    """
    aplica o algoritmo A* para resolver o quebra cabeça.
    """
    abertos = []  # lista abertos sera uma heap para estados a serem abertos(explorados)
    heapq.heappush(abertos, (heuristica(inicial, objetivo), 0, inicial, []))  # fila começa com o estado inicial: (custo estimado f, custo acumulado g, estado atual, caminho percorrido).
    fechados = set()  # estados já abertos, uso de set para otimizar 

    while abertos:
        _, g, estado_atual, caminho = heapq.heappop(abertos) #  remove o estado com o menor custo f da fila de abertos e ignoramos o custo f da tupla ja que queremos somente g

        if estado_atual == objetivo:# se o estado atual for o objetivo, retorna o caminho encontrado, o numero de nós (retorna g(n) a fim de experimentação)
            return caminho + [estado_atual], len(fechados), g 

        if tuple(estado_atual) in fechados: # se estado atual ja tiver sido aberto, vai para o proximo
            continue

        fechados.add(tuple(estado_atual)) # se nao, marca atual como fechado

        for novo_estado in gera_novos_estados(estado_atual): #gera todos os tabuleiros possiveis (estados) a partir do atual chamando a gera_novos_estados.
            if tuple(novo_estado) not in fechados: # estado é uma tupla para poder armazenar set e comparar o set fechado
                novo_caminho = caminho + [estado_atual] # adiciona a lista do estado atual (unico elemento) a lista de caminhos para gerar novo caminho possivel
                novo_g = g + 1 # atualiza g (custo uniforme, cada movimento tem custo 1).
                f = novo_g + heuristica(novo_estado, objetivo) # f é a função de avaliação que soma o custo acumulado g a estimativa heurística h (para prioridade a estados de menor custo)
                heapq.heappush(abertos, (f, novo_g, novo_estado, novo_caminho)) # da o push adicionando o novo estado na fila de abertos com sua prioridade (f).

    return None, len(fechados) # se nao tiver retorna none

def imprime_tabuleiro(tabuleiro):
    """
    Imprime o tabuleiro em uma forma 3x3.
    """
    for i in range(0, 9, 3): # de 0 a 9 de 3 em 3
        print(tabuleiro[i:i+3]) #slicing pegando 3 elementos a partir do indice i
    print()

def imprime_solucao(caminho):
    """
    Imprime os passos da solução,
    O custo acumulado g(n) acaba sendo o mesmo (novo_estado com custo uniforme = 1) em um caminho otimo.
    """
    for estado in caminho:
        imprime_tabuleiro(estado)
    print("Quantidade de passos para a solução g(n):", len(caminho) - 1) # -1 para não contar o estado inicial mas não é um movimento do jogo

def main():
    # estados para os experimentos
    config_inicial_1 = ["x", "o", "x",
                        "o", "x", "o",
                        "_", "_", "_"]
    
    config_inicial_2 = ["x", "o", "x",
                         "o", "o", "x",
                         "_", "_", "_"]

    config_inicial_3 = ["o", "_", "x",
                        "_", "x", "_",
                        "o", "_", "_"]
    


    escolha = int(input("Escolha o experimento a ser executado: \n- Experimento 1 (digite 1)\n- Experimento 2 (digite 2):\n- Experimento 3 (digite 3):\n "))

    if escolha == 1:
        estado_inicial = config_inicial_1
    elif escolha == 2:
        estado_inicial = config_inicial_2
    elif escolha == 3:
        estado_inicial = config_inicial_3
    else:
        print("Escolha inválida, por favor digite 1, 2 ou 3!")
        return
    
    
    print("------------------------------------------")

    # heurística naive de peças fora do lugar
    tempo_inicial = time.time()
    solucao, nos_gerados_h1, g_h1 = a_estrela(estado_inicial, estado_objetivo, h_naive) # usamos callback function passando h_naive
    tempo_final = time.time()
    
    if solucao is None:
        print("Nenhuma solução foi encontrada com a heurística das peças fora do lugar.")
    else:
        print("Heurística das peças fora do lugar:\n")
        imprime_solucao(solucao)
        print(f"Nós gerados: {nos_gerados_h1} Tempo: {tempo_final - tempo_inicial:.6f} segundos\n")

    print("------------------------------------------")

    # heurística da distância Manhattan
    tempo_inicial = time.time()
    solucao, nos_gerados_h2, g_h2 = a_estrela(estado_inicial, estado_objetivo, h_manhattan)
    tempo_final = time.time()
    
    if solucao is None:
        print("Nenhuma solução foi encontrada com a heurística da distância Manhattan.")
    else:
        print("Heurística da distância Manhattan:\n")
        imprime_solucao(solucao)
        print(f"Nós gerados: {nos_gerados_h2} Tempo: {tempo_final - tempo_inicial:.6f} segundos")

if __name__ == "__main__":
    main()
