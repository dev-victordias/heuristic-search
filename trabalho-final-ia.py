# -- coding: utf-8 --
author = "Victor Dias"

import sys
import csv
from math import sqrt
from math import pow

custo_total = 0

# Given an array and a value, find the coordinates (i,j)
# that contain the searched value and returns them in a list.
def encontraPosicoes (matriz, M, N, valor):
	posicoes = []
	for i in range(0, M):
		for j in range(0, N):
			if matriz[i][j] == valor:
				posicoes.append((i, j))
	return posicoes

# Given an initial state and a list of final states, sort
# the list of end states based on Euclidean distance
# in a new list and returns it.
def ordenaEstados (estado_inicial, estados_finais):
	x = estado_inicial[0]
	y = estado_inicial[1]
	estados_ordenados = {}

	for estado_final in estados_finais:
		x_estado_final = estado_final[0]
		y_estado_final = estado_final[1]
		diff1 = x_estado_final - x
		diff2 = y_estado_final - y
		somaDiffs = pow(diff1, 2) + pow(diff2, 2)
		distancia_atual = sqrt(somaDiffs)
		estados_ordenados[estado_final] = distancia_atual
		estados_finais_ordenados = {}
		keys_ordenadas = {}
	
	i = 0
	for item in sorted(estados_ordenados, key = estados_ordenados.get):
		estados_finais_ordenados[i] = estados_ordenados[item]
		keys_ordenadas[i] = item
		i = i + 1
	return list(keys_ordenadas.values())

# Given an array and the current position by coordinates (i,j),
# find successor states within 1 step of (i,j).
def encontra_estados_sucessores (matriz, M, N, posicao_atual):
	i = posicao_atual[0]
	j = posicao_atual[1]
	estados_sucessores = []
	if i > 0: # Moves up in the matrix.
		estados_sucessores.append ((i-1, j))
	if i+1 < M: # Moves down in the matrix.
		estados_sucessores.append ((i+1, j))
	if j > 0: # Moves left in the matrix.
		estados_sucessores.append ((i, j-1))
	if j+1 < N: # Moves right in the matrix.
		estados_sucessores.append ((i, j+1))
	return estados_sucessores

# Given a state considered final, a list of predecessors and an iteration number,
# shows in which iteration the solution was found and how to start from the initial state
# and get to the final state from the partial solution stored in predecessors,
# in addition, set the partial path cost to that path.
def apresenta_solucao (matriz, estado, predecessores, iteracao):
	custo = 0
	caminho = []
	caminho.append(estado)
	print("Solucao encontrada na iteracao " + str(iteracao) + ":")
	while predecessores[estado] != None:
		caminho.append(predecessores[estado])
		estado = predecessores[estado]
	caminho = caminho[::-1]
	print("Caminho encontrado: ")
	print(caminho)
	for elemento in caminho:
		x = elemento[0]
		y = elemento[1]
		custo = custo + int(matriz[x][y])
	custo -= 20
	global custo_total 
	custo_total += custo
	print("\nCusto do caminho: ")
	print(custo)
	print("\n\n")
		
# Given any state and a set of final states,
# calculates the distance from any state to the nearest final state.
def calcula_distancia_euclidiana (estado, estados_finais):
	x = estado[0]
	y = estado[1]
	distancia_minima = 1000000000

	for estado_final in estados_finais:
		x_estado_final = estado_final[0]
		y_estado_final = estado_final[1]
		diff1 = x_estado_final - x
		diff2 = y_estado_final - y
		somaDiffs = pow(diff1, 2) + pow(diff2, 2)
		distancia_atual = sqrt(somaDiffs)
		if distancia_atual < distancia_minima:
			distancia_minima = distancia_atual
	return distancia_minima

# Given a set of nodes and a heuristic function,
# finds the lowest-valued state in this set.
def encontra_estado_mais_promissor (nodes, heuristica_estados):
	valor_mais_promissor = 1000000000
	indice_mais_promissor = 0
	indice = 0
	for estado in nodes:
		if heuristica_estados[estado] < valor_mais_promissor:
			valor_mais_promissor = heuristica_estados[estado]
			indice_mais_promissor = indice
		indice = indice + 1
	return indice_mais_promissor

# A* Search Algorithm
def busca_a_estrela (matriz, M, N, estado_inicial, estados_finais):
	distancia_euclidiana = {}
	distancia_percorrida = {}
	heuristica = {}
	predecessores = {}
	estados_expandidos = []
	solucao_encontrada = False

	print("\nAlgoritmo A*\n")

	# initialization of the distance traveled (f), distance to the goal (g) and heuristic (h = f+g).
	distancia_percorrida[estado_inicial] = 0
	distancia_euclidiana[estado_inicial] = calcula_distancia_euclidiana (estado_inicial, estados_finais) 
	heuristica[estado_inicial] = distancia_percorrida[estado_inicial] + distancia_euclidiana[estado_inicial]
	predecessores[estado_inicial] = None
	print("Heuristica da Distância no Estado Inicial: " + str(heuristica[estado_inicial]))
	nodes = []
	nodes.append(estado_inicial)
	iteracao = 1
	while len(nodes) != 0:
		indice_mais_promissor = encontra_estado_mais_promissor(nodes, heuristica)
		estado = nodes.pop(indice_mais_promissor)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores(matriz, M, N, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):	
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in nodes:
				nodes.append(sucessor)
				if sucessor not in heuristica.keys():
					linha = sucessor[0]
					coluna = sucessor[1]
					distancia_euclidiana[sucessor] = calcula_distancia_euclidiana(sucessor, estados_finais)
					distancia_percorrida[sucessor] = distancia_percorrida[estado] + int(matriz[linha][coluna])
					heuristica[sucessor] = distancia_euclidiana[sucessor] + distancia_percorrida[sucessor]
					predecessores[sucessor] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		apresenta_solucao (matriz, estado, predecessores, iteracao)
	else:
		print("Nao foi possivel encontrar uma solucao para o problema.")

def main():
	if len(sys.argv) == 2:
		count = 0
		problema = sys.argv[1]

		# load the csv file containing the map representation
		with open (problema, 'r') as csv_file:
			leitor_problema = csv.reader(csv_file)
			entrada = list(leitor_problema)
	
		M = int(entrada[0][0]) # number of lines.
		N = int(entrada[0][1]) # number of cols.
		matriz = entrada[1:]   # map represented as matrix.

		# calculates the initial and final states based on the parameter
		estado_inicial = encontraPosicoes (matriz, M, N, '1')
		estados_finais = encontraPosicoes (matriz, M, N, '0')

		# finds the best paths for each pendant
		while(count < 3):
			print("Estado Inicial: " + str(estado_inicial))
			print("Estado Final: " + str(estados_finais))

			estado_final = ordenaEstados(estado_inicial[0], estados_finais)
			busca_a_estrela (matriz, M, N, estado_inicial[0], [tuple(estado_final[0])])
			estado_inicial = [estado_final[0]]

			if(len(estados_finais) > 0):
				estados_finais.remove(estado_inicial[0])
				matriz[estado_inicial[0][0]][estado_inicial[0][1]] = 20
			count = count + 1
	
		# find the best way to the Master Sword
		estados_finais = encontraPosicoes (matriz, M, N, '2')
		busca_a_estrela(matriz, M, N, estado_inicial[0], estados_finais)

		print("Custo total: ")
		print(custo_total)
			
	else:
		print("Forneca um arquivo CSV para os algoritmos de busca.")

if __name__ == "__main__":
    main()
