import networkx as nx
import matplotlib as plt
import xml.etree.ElementTree as ET
import subprocess
import sys
import colorama
from colorama import Fore, Back, Style, init
# Função para ler um grafo a partir de um arquivo GraphML e definir pesos nas arestas
def ler_grafo(file_path):
    grafo = nx.Graph()

    tree = ET.parse(file_path)
    root = tree.getroot()

    for node in root.findall(".//node"):
        grafo.add_node(node.get("id"))

    for edge in root.findall(".//edge"):
        source = edge.get("source")
        target = edge.get("target")

        weight = float(edge.get("weight"))
        if weight is not None:
            grafo.add_edge(source, target, weight=weight)  # Passando o peso da aresta
        else:
            grafo.add_edge(source, target, weight=1.0)


    return grafo
# Função para retornar a ordem do grafo
def ordem_do_grafo(grafo):
    return grafo.order()

# Função para retornar o tamanho do grafo
def tamanho_do_grafo(grafo):
    return grafo.size()

# Função para retornar os vizinhos de um vértice fornecido
def vizinhos_do_vertice(grafo, vertice):
    return list(grafo.neighbors(vertice))

# Função para determinar o grau de um vértice fornecido
def grau_do_vertice(grafo, vertice):
    return grafo.degree(vertice)

# Função para retornar a sequência de graus do grafo
def sequencia_de_graus(grafo):
    sequencia_graus = [grau for _, grau in grafo.degree()]
    return sorted(sequencia_graus, reverse=True)

# Função para determinar a excentricidade de um vértice (considerando pesos)
def excentricidade(grafo, vertice):
    if any("weight" in grafo[u][v] for u, v in grafo.edges):
        excentricidades = nx.eccentricity(grafo,weight='weight')
    else:
        excentricidades = nx.eccentricity(grafo)

    return excentricidades[vertice]

# Função para determinar o raio do grafo (considerando pesos)
def raio_do_grafo(grafo):
    if any("weight" in grafo[u][v] for u, v in grafo.edges):
        radius = nx.radius(grafo, weight='weight')
    else:
        radius = nx.radius(grafo)

    return radius

# Função para determinar o diâmetro do grafo (considerando pesos)
def diametro_do_grafo(grafo):
    if any("weight" in grafo[u][v] for u, v in grafo.edges):
        return nx.diameter(grafo,weight='weight')
    else:
        return nx.diameter(grafo)



# Função para determinar o centro do grafo
def centro_do_grafo(grafo):
    return nx.center(grafo)

# Função para determinar a árvore de busca em largura
def arvore_de_busca_em_largura(grafo, v):
    output = ""
    output += f"\n\tBusca em Largura:\n"

    print(f"{Fore.GREEN}\n\tBusca em Largura:{Fore.RESET}\n")

    vertice_inicial = v
    visitado = set()
    fila = []
    visitados_sequence = []  # para manter a sequência de vértices visitados
    nao_arvore = []  # para armazenar as arestas que não fazem parte da árvore de busca
    visitado.add(v)
    fila.append(v)
    visitados_sequence.append(v)

    G = nx.Graph()  # Cria um gráfico vazio

    while fila:
        v = fila.pop(0)
        for w in grafo[v]:
            if w not in visitado:
                explore(v, w)
                fila.append(w)
                visitado.add(w)
                visitados_sequence.append(w)
                G.add_edge(v, w)  # adiciona a aresta ao gráfico
            else:
                if (v, w) not in G.edges:
                    nao_arvore.append((v, w))
                    explore(v, w)

    nx.write_graphml(G, "arvore_busca.graphml")  # salva o gráfico como um arquivo GraphML

    print("\n" + Fore.MAGENTA + "Sequência de vértices visitados na busca em largura:" + Fore.RESET + "", visitados_sequence)
    print("\n" + Fore.MAGENTA + "Aresta(s) que não faz(em) parte da árvore de busca em largura:" + Fore.RESET + "", nao_arvore)


    output += "\n" + f"Sequência de vértices visitados na busca em largura: {visitados_sequence}\n"
    output += "\n" + f"Aresta(s) que não faz(em) parte da árvore de busca em largura: {nao_arvore}\n"

    return output

def explore(v, w):
    print(f"{Fore.YELLOW}\tExplorando aresta entre {Fore.RESET} {v} e {w}")


# Função para determinar distância e caminho mínimo (considerando pesos)
def distancia_e_caminho_minimo(grafo, origem, destino):
    try:
        if any("weight" in grafo[u][v] for u, v in grafo.edges):
            caminho_minimo = nx.shortest_path(grafo, source=origem, target=destino, weight='weight')
            distancia = nx.shortest_path_length(grafo, source=origem, target=destino, weight='weight')
        else:
            caminho_minimo = nx.shortest_path(grafo, source=origem, target=destino)
            distancia = nx.shortest_path_length(grafo, source=origem, target=destino)

        return distancia, caminho_minimo
    except nx.NetworkXNoPath:
        return "Não há caminho entre os vértices."

# Função para determinar a centralidade de proximidade C de um vértice
def centralidade_de_proximidade_C(grafo, vertice):
    N = grafo.order()
    distancias = nx.single_source_shortest_path_length(grafo, vertice)
    total_distancias = sum(distancias.values())
    if total_distancias == 0:
        return 0.0
    return (N - 1) / total_distancias

