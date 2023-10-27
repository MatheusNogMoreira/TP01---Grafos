import grafo
import networkx as nx
import matplotlib.pyplot as plt
from colorama import Fore, Back, Style, init

init(autoreset=True)

def menu():
    print(Back.LIGHTBLUE_EX + "====== Menu ======" + Style.RESET_ALL)
    print(Fore.CYAN + "[1] " + Fore.RESET + "Ler grafo")
    print(Fore.CYAN + "[2]. " + Fore.RESET + "Ordem do grafo")
    print(Fore.CYAN + "[3]. " + Fore.RESET + "Tamanho do grafo")
    print(Fore.CYAN + "[4]. " + Fore.RESET + "Vizinhos de um vértice")
    print(Fore.CYAN + "[5]. " + Fore.RESET + "Grau de um vértice")
    print(Fore.CYAN + "[6]. " + Fore.RESET + "Sequência de graus do grafo")
    print(Fore.CYAN + "[7]. " + Fore.RESET + "Excentricidade de um vértice")
    print(Fore.CYAN + "[8]. " + Fore.RESET + "Raio do grafo")
    print(Fore.CYAN + "[9]. " + Fore.RESET + "Diâmetro do grafo")
    print(Fore.CYAN + "[10]. " + Fore.RESET + "Centro do grafo")
    print(Fore.CYAN + "[11]. " + Fore.RESET + "Busca em Largura e Árvore de Largura (em GraphML)")
    print(Fore.CYAN + "[12]. " + Fore.RESET + "Distância e Caminho Mínimo")
    print(Fore.CYAN + "[13]. " + Fore.RESET + "Centralidade de Proximidade C")
    print(Fore.RED + "0. " + Fore.RESET + "Sair")

if __name__ == "__main__":
    grafo_atual = None

    while True:
        menu()
        escolha = input(Fore.CYAN + "Escolha uma opção (ou " + Fore.RED + "'0'" + Fore.CYAN + " para sair): " + Fore.RESET)

        if escolha == '1':
            arquivo_grafo = input(Fore.YELLOW + "Informe o caminho para o arquivo GraphML: " + Fore.RESET)
            grafo_atual = grafo.ler_grafo(arquivo_grafo)
            if grafo_atual:
                print(Fore.GREEN + "Grafo carregado com sucesso." + Fore.RESET)
        elif escolha == '2':
           
            if grafo_atual:
                ordem = grafo.ordem_do_grafo(grafo_atual)
                print(Fore.MAGENTA + "Ordem do grafo:" + Fore.RESET, ordem)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '3':
            if grafo_atual:
                tamanho = grafo.tamanho_do_grafo(grafo_atual)
                print(Fore.MAGENTA + "Tamanho do grafo:" + Fore.RESET, tamanho)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '4':
            if grafo_atual:
                vertice = int(input(Fore.YELLOW + "Informe o vértice: " + Fore.RESET))
                if (vertice < 1 or vertice > grafo.ordem_do_grafo(grafo_atual)):
                    print(Fore.RED + "Erro: VERTICE INVALIDO" + Fore.RESET)
                else:
                    vizinhos = grafo.vizinhos_do_vertice(grafo_atual, vertice)
                    print(Fore.MAGENTA + "Vizinhos de" + Fore.RESET, vertice, ":", vizinhos)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '5':
            if grafo_atual:
                vertice = int(input(Fore.YELLOW + "Informe o vértice: " + Fore.RESET))
                if (vertice < 1 or vertice > grafo.ordem_do_grafo(grafo_atual)):
                    print(Fore.RED + "Erro: VERTICE INVALIDO" + Fore.RESET)
                else:
                    grau = grafo.grau_do_vertice(grafo_atual, str(vertice))
                    print(Fore.MAGENTA + "Grau de" + Fore.RESET, vertice, ":", grau)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '6':
            if grafo_atual:
                sequencia = grafo.sequencia_de_graus(grafo_atual)
                print(Fore.MAGENTA + "Sequência de graus do grafo:" + Fore.RESET, sequencia)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '7':
            if grafo_atual:
                vertice = input(Fore.YELLOW + "Informe o vértice: " + Fore.RESET)
                excentricidade = grafo.excentricidade(grafo_atual, str(vertice))
                print(Fore.MAGENTA + "Excentricidade de" + Fore.RESET, vertice, ":", excentricidade)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '8':
            if grafo_atual:
                raio = grafo.raio_do_grafo(grafo_atual)
                print(Fore.MAGENTA + "Raio do grafo:" + Fore.RESET, raio)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '9':
            if grafo_atual:
                diametro = grafo.diametro_do_grafo(grafo_atual)
                print(Fore.MAGENTA + "Diâmetro do grafo:" + Fore.RESET, diametro)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '10':
            if grafo_atual:
                centro = grafo.centro_do_grafo(grafo_atual)
                print(Fore.MAGENTA + "Centro do grafo:" + Fore.RESET, centro)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '11':
            if grafo_atual:
                vertice_inicial = input(Fore.YELLOW + "Informe o vértice inicial para a busca em largura: " + Fore.RESET)

                grafo.arvore_de_busca_em_largura(grafo_atual, str(vertice_inicial))
                print(Fore.GREEN + "Árvore de busca em largura gerada e salva em 'arvore_busca.graphml'." + Fore.RESET)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '12':
            if grafo_atual:
                origem = input(Fore.YELLOW + "Informe o vértice de origem: " + Fore.RESET)
                destino = input(Fore.YELLOW + "Informe o vértice de destino: " + Fore.RESET)
                distancia, caminho_minimo = grafo.distancia_e_caminho_minimo(grafo_atual, str(origem), str(destino))
                if distancia != float('inf'):
                    print(Fore.MAGENTA + f"Distância mínima de {origem} para {destino}:" + Fore.RESET, distancia)
                    print(Fore.MAGENTA + "Caminho mínimo:" + Fore.RESET, caminho_minimo)
                else:
                    print(Fore.RED + "Não há caminho entre os vértices." + Fore.RESET)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '13':
            if grafo_atual:
                vertice = input(Fore.YELLOW + "Informe o vértice para calcular a centralidade de proximidade C: " + Fore.RESET)
                centralidade_c = grafo.centralidade_de_proximidade_C(grafo_atual, str(vertice))
                print(Fore.CYAN + f"Centralidade de proximidade C de {vertice}:" + Fore.RESET, centralidade_c)
            else:
                print(Fore.RED + "Grafo não carregado." + Fore.RESET)
        elif escolha == '0':
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente." + Fore.RESET)