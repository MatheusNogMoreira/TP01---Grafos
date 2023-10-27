import os
import subprocess
import sys
import tkinter as tk
import networkx as nx
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox, Menu
import PIL
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import grafo


class Main:
    def __init__(self):
        self.grafo_atual = None
        self.JanelaTk = None
        self.TipoFonte = "Arial"
        self.TamanhoFonte = 12
        self.current_path = os.getcwd()
        self.ComprimentoJanela = 700
        self.AlturaJanela = 1125
        self.icone_path = self.current_path + "/Imagens/icone.png"
        self.main()

    def get_vertice(self, texto_pergunta):
        toplevel = tk.Toplevel(self.JanelaTk,bg='white')
        toplevel.resizable(False, False)
        toplevel.iconphoto(True, tk.PhotoImage(file=self.icone_path))

        Fechou_Ou_Cancelou = [False]

        self.valor_vertice_escolhido = tk.StringVar()

        l1 = tk.Label(toplevel, text=texto_pergunta,bg='white')
        l1.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        entry = tk.Entry(toplevel, textvariable=self.valor_vertice_escolhido,bg='white')
        entry.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        def ok_button_click():
            toplevel.destroy()

        def fechar_janela():
            Fechou_Ou_Cancelou[0] = True
            toplevel.destroy()

        b1 = tk.Button(toplevel, text="Ok", command=ok_button_click, width=10,bg='white')
        b1.grid(row=2, column=0, padx=(10, 0), pady=10)

        def cancelar_button_click():
            Fechou_Ou_Cancelou[0] = True
            toplevel.destroy()

        b2 = tk.Button(toplevel, text="Cancelar", command=cancelar_button_click, width=10,bg='white')
        b2.grid(row=2, column=1, padx=(0, 10), pady=10)

        toplevel.protocol("WM_DELETE_WINDOW", fechar_janela)

        toplevel.update_idletasks()

        window_width = toplevel.winfo_reqwidth()
        window_height = toplevel.winfo_reqheight()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        toplevel.geometry(f"{window_width}x{window_height}+{x}+{y}")

        toplevel.wait_window(toplevel)

        if Fechou_Ou_Cancelou[0]:
            return -1
        vertice_escolhido = self.valor_vertice_escolhido.get()
        if self.grafo_atual.has_node(vertice_escolhido):
            return vertice_escolhido
        else:
            self.mostrar_erro("Vértice Não Existente!", "O vértice escolhido não existe no grafo!")
            return self.get_vertice(texto_pergunta)

    def mostrar_resultado(self, texto):
        toplevel = tk.Toplevel(self.JanelaTk,bg='white')
        toplevel.resizable(False, False)
        toplevel.iconphoto(True, tk.PhotoImage(file=self.icone_path))

        self.valor_vertice_escolhido = tk.StringVar()

        l1 = tk.Label(toplevel, text=texto,bg='white')
        l1.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        def ok_button_click():
            toplevel.destroy()

        def fechar_janela():
            toplevel.destroy()

        b1 = tk.Button(toplevel, text="Ok", command=ok_button_click, width=10,anchor=tk.CENTER,bg='white')
        b1.grid(row=1, column=0, columnspan=2, pady=10)

        toplevel.protocol("WM_DELETE_WINDOW", fechar_janela)

        toplevel.update_idletasks()

        window_width = toplevel.winfo_reqwidth()
        window_height = toplevel.winfo_reqheight()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        toplevel.geometry(f"{window_width}x{window_height}+{x}+{y}")

        toplevel.wait_window(toplevel)

    def tamanho_figura(self,Grafo):
        num_nodes = len(Grafo.nodes())
        num_edges = len(Grafo.edges())


        fig_width = max(3, num_nodes * 0.5)
        fig_height = max(3, num_nodes * 0.5)

        return fig_width, fig_height
    def configurar_fonte(self, widget):
        font = (self.TipoFonte, self.TamanhoFonte)
        widget.config(font=font)

    def converter_imagem(self, nome_arquivo, output):
        try:
            is_bfs_graph = self.is_bfs_graph(nome_arquivo)

            if is_bfs_graph:
                G = nx.read_graphml(nome_arquivo)
                layout = nx.spring_layout(G)
                show_edge_labels = False
            else:
                G = self.load_common_graph(nome_arquivo)
                layout = nx.circular_layout(G)
                show_edge_labels = True

            for node in G.nodes():
                new_label = int(G.nodes[node].get('mainText', node))
                G.nodes[node]['label'] = str(new_label)
            tamanho_figura_x,tamanho_figura_y = self.tamanho_figura(G)
            plt.figure(figsize=(tamanho_figura_x, tamanho_figura_y))
            ax = plt.gca()

            labels = {node: G.nodes[node].get('label', '') for node in G.nodes()}
            nx.draw(G, layout, with_labels=False, node_size=100, ax=ax)
            nx.draw_networkx_labels(G, layout, labels, font_size=12, font_color='black')

            if show_edge_labels:
                edge_labels = {(u, v): d.get('weight', 1) for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, layout, edge_labels, font_size=10)

            plt.savefig(output, format="png", bbox_inches="tight")
            plt.close()

            return True

        except Exception as e:
            print(f"Erro: {e}")
            return False

    def is_bfs_graph(self, nome_arquivo):
        with open(nome_arquivo, 'r') as file:
            content = file.read()
            return (
                    "graph edgedefault=\"directed\"" in content or
                    "<graph edgedefault=" in content
            )

    def load_common_graph(self, nome_arquivo):
        G = nx.Graph()
        tree = ET.parse(nome_arquivo)
        root = tree.getroot()

        if root.tag == '{http://graphml.graphdrawing.org/xmlns}graph':
            for edge in root.iter('edge'):
                source = int(edge.get('source'))
                target = int(edge.get('target'))
                weight = float(edge.get('weight', 1))
                G.add_edge(source, target, weight=weight)
        elif root.tag == 'graphml':
            for edge in root.iter('edge'):
                source = int(edge.get('source'))
                target = int(edge.get('target'))
                weight = float(edge.get('weight', 1))
                G.add_edge(source, target, weight=weight)

        return G
    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(title=titulo, message=mensagem)

    def mostrar_aviso(self, titulo, mensagem):
        messagebox.showinfo(title=titulo, message=mensagem)

    def centralizar_tela(self, width, height):
        ws = self.JanelaTk.winfo_screenwidth()
        x = (ws / 2) - (width / 2)
        y = 0

        self.JanelaTk.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def carregar_grafo(self):
        file_types = [("GraphML Files", "*.graphml")]
        nome_arquivo = filedialog.askopenfilename(initialdir=self.current_path, filetypes=file_types)
        if not nome_arquivo:
            return None
        try:
            self.grafo_atual = grafo.ler_grafo(nome_arquivo)
        except FileNotFoundError:
            self.mostrar_erro("Grafo Inválido","Esse grafo é inválido!")
            return None

        if self.grafo_atual:
            self.status_label.config(text=f"Grafo Atual: {os.path.basename(nome_arquivo)}")
            Image_Path = os.path.dirname(nome_arquivo) + "/Imagens/" + os.path.basename(nome_arquivo) + ".png"

            self.JanelaTk.geometry(f"{self.AlturaJanela}x{self.ComprimentoJanela}")
            self.centralizar_tela(self.AlturaJanela,self.ComprimentoJanela)
            if self.converter_imagem(nome_arquivo, Image_Path):
                self.colocar_grafo(Image_Path)

                self.set_buttons_visibility(True)
            else:
                self.mostrar_erro("Erro", "Falha ao converter o grafo para imagem")

        else:
            self.mostrar_erro("Erro", "Grafo não carregado")

    def carrega_e_mostra_graph_imagem(self,image_file):
        try:
            img = Image.open(image_file)
            img.thumbnail((450, 370), Image.LANCZOS)
            graph_image = ImageTk.PhotoImage(img)
            return graph_image

        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")
    def colocar_grafo(self,image_file):
        grafo_imagem = self.carrega_e_mostra_graph_imagem(image_file)
        self.image_frame2 = tk.Frame(self.image_frame, bg="white")
        self.image_frame2.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        img_label = tk.Label(self.image_frame2, image=grafo_imagem,bg="white")
        img_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.status_label.place(relx=0.45, rely=0.02)

        img_label.image = grafo_imagem

    def colocar_grafo_arvore(self, image_file,vertice):
        Image_Path = os.path.dirname(image_file) + "Imagens/" + os.path.basename(image_file) + ".png"
        self.converter_imagem(image_file, Image_Path)
        grafo_imagem = self.carrega_e_mostra_graph_imagem(Image_Path)
        self.image_frame_arvore = tk.Frame(self.image_frame2, bg="white")
        self.label_arvore = tk.Label(self.image_frame_arvore,bg='white',text=f"Árvore de Busca Resultante para o Vértice {vertice}: ")
        self.configurar_fonte(self.label_arvore)
        self.label_arvore.grid(row=0,column=0,padx=0,pady=0,sticky="nsew")
        self.image_frame_arvore.grid(row=0, column=1, padx=350, pady=0, sticky="nsew")

        img_label = tk.Label(self.image_frame_arvore, image=grafo_imagem, bg="white")
        img_label.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        img_label.image = grafo_imagem
    def sequencia_graus_grafo(self):
        if self.grafo_atual:
            sequencia = grafo.sequencia_de_graus(self.grafo_atual)
            self.mostrar_resultado(f"Sequência de graus do grafo:\n" + " ".join(str(sequencia)))

    def excentricidade_vertice(self):

        if self.grafo_atual:
            vertice = self.get_vertice("Digite qual vértice que deseja analisar:")
            if vertice != -1:
                excentricidade = grafo.excentricidade(self.grafo_atual,vertice)
                self.mostrar_resultado(f"Excentricidade do vértice {vertice}: {excentricidade}")

    def ordem_grafo(self):
        if self.grafo_atual:
            ordem = grafo.ordem_do_grafo(self.grafo_atual)
            self.mostrar_resultado(f"Ordem do grafo: {ordem}")
        else:
            self.mostrar_erro("Erro", "Grafo não carregado")

    def centralidade_de_proximidade_C(self):
            if self.grafo_atual:
                vertice = self.get_vertice("Digite qual vértice que deseja analisar:")
                if(vertice != -1):
                    centralidade_proximidade_c = grafo.centralidade_de_proximidade_C(self.grafo_atual,vertice)
                    self.mostrar_resultado(f"A centralidade de Proximidade C do Vértice {vertice} é: {centralidade_proximidade_c:.3f}")
    def arvore_busca(self):

        if self.grafo_atual:
            vertice = self.get_vertice("Digite o vértice inicial:")
            if(vertice != -1):
                bfs_tree = grafo.arvore_de_busca_em_largura(self.grafo_atual, vertice)
                #nx.write_graphml(bfs_tree, "arvore_busca_largura.graphml")
                self.colocar_grafo_arvore("arvore_busca.graphml",vertice)
                self.mostrar_resultado(bfs_tree)


        else:
            self.mostrar_erro("Erro", "Grafo não carregado")
    def distancia_e_caminho_minimo(self):
        vertice_inicial = self.get_vertice("Digite qual será o vértice inicial:")
        vertice_final = self.get_vertice("Digite qual será o vértice final:")
        if self.grafo_atual and vertice_inicial != -1 and vertice_final !=1:
            Resultados = grafo.distancia_e_caminho_minimo(self.grafo_atual, vertice_inicial, vertice_final)
            if(Resultados):
                distancia, caminho_minimo = Resultados
                if distancia != float('inf'):
                    self.mostrar_resultado(f"Distância mínima de {vertice_inicial} para {vertice_final}: {int(distancia)}\nCaminho mínimo: {caminho_minimo}")
            else:
                self.mostrar_resultado("Não há caminho entre os vértices.")

    def vizinhos_vertice(self):
        vertice = self.get_vertice("Digite qual vértice que deseja analisar:")
        if self.grafo_atual and vertice != -1:
            vizinhos = grafo.vizinhos_do_vertice(self.grafo_atual, vertice)
            self.mostrar_resultado(f"Vizinhos do vértice {vertice}:\n {'-'.join(vizinhos)}")

    def grau_vertice(self):
        vertice = self.get_vertice("Digite qual vértice que deseja analisar:")
        if self.grafo_atual and vertice != -1:
            Grau_Vertice = grafo.grau_do_vertice(self.grafo_atual, vertice)
            self.mostrar_resultado(f"Graus do vértice {vertice}: {str(Grau_Vertice)}")
    def tamanho_grafo(self):
        if self.grafo_atual:
            tamanho = grafo.tamanho_do_grafo(self.grafo_atual)
            self.mostrar_resultado(f"Tamanho do grafo: {tamanho}")
        else:
            self.mostrar_erro("Erro", "Grafo não carregado")

    def sair(self):
        self.JanelaTk.destroy()

    def button_hover(self,event):
        event.widget.config(bg="lightblue")

    def button_leave(self,event):
        event.widget.config(bg="white")

    def mostrar_centro_do_grafo(self):
        if self.grafo_atual:
            centro = grafo.centro_do_grafo(self.grafo_atual)
            self.mostrar_resultado(f"Centro do grafo: {centro}")
        else:
            self.mostrar_erro("Erro", "Grafo não carregado")

    def mostrar_raio_do_grafo(self):
        if self.grafo_atual:
            raio = grafo.raio_do_grafo(self.grafo_atual)
            self.mostrar_resultado(f"Raio do grafo: {raio}")
        else:
            self.mostrar_erro("Erro", "Grafo não carregado")

    def mostrar_diametro_do_grafo(self):
        if self.grafo_atual:
            diametro = grafo.diametro_do_grafo(self.grafo_atual)
            self.mostrar_resultado(f"Diâmetro do grafo: {diametro}")
        else:
            self.mostrar_erro("Erro", "Grafo não carregado")

    def main(self):
        self.JanelaTk = tk.Tk()
        self.JanelaTk.iconphoto(True, tk.PhotoImage(file=self.icone_path))
        #self.JanelaTk.resizable(False, False)
        self.JanelaTk.configure(bg="white")
        self.JanelaTk.title("Menu Grafo")
        self.JanelaTk.geometry("200x200")
        main_menu = Menu(self.JanelaTk)
        self.JanelaTk.config(menu=main_menu)
        main_menu.add_command(label="Carregar Grafo", command=self.carregar_grafo)
        main_menu.add_command(label="Sair", command=self.JanelaTk.destroy)

        self.image_frame = tk.Frame(self.JanelaTk, bg="white")
        self.image_frame.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

        self.frame_botao = tk.Frame(self.JanelaTk, bg="white")
        self.frame_botao.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.button_width = 27
        self.button_height = 2

        ordem_button = tk.Button(self.frame_botao, text="Ordem do Grafo", command=self.ordem_grafo)
        tamanho_button = tk.Button(self.frame_botao, text="Tamanho do Grafo", command=self.tamanho_grafo)
        arvore_button = tk.Button(self.frame_botao,text="Árvore de Busca",command=self.arvore_busca)
        vizinhos_vertice_button = tk.Button(self.frame_botao,text="Vizinhos de um Vértice",command = self.vizinhos_vertice)
        graus_vertice_button = tk.Button(self.frame_botao, text="Graus de um Vértice",command=self.grau_vertice)
        sequencia_graus_grafo_button = tk.Button(self.frame_botao, text="Sequência de Graus do Grafo",command=self.sequencia_graus_grafo)
        excentricidade_vertice_button = tk.Button(self.frame_botao, text="Excentricidade de um Vértice",command=self.excentricidade_vertice)
        distancia_caminho_minimo_button = tk.Button(self.frame_botao,text="Distância e Caminho Mínimo",command=self.distancia_e_caminho_minimo)
        centralidade_proximidade_c_button =tk.Button(self.frame_botao,text="Centralidade de Proximidade C",command=self.centralidade_de_proximidade_C)

        self.configurar_fonte(ordem_button)
        self.configurar_fonte(tamanho_button)
        self.configurar_fonte(vizinhos_vertice_button)
        self.configurar_fonte(sequencia_graus_grafo_button)
        self.configurar_fonte(excentricidade_vertice_button)
        self.configurar_fonte(distancia_caminho_minimo_button)
        self.configurar_fonte(centralidade_proximidade_c_button)

        ordem_button.config(width=self.button_width, height=self.button_height, bg="white")
        tamanho_button.config(width=self.button_width, height=self.button_height, bg="white")
        arvore_button.config(width=self.button_width, height=self.button_height, bg="white")
        vizinhos_vertice_button.config(width=self.button_width,height=self.button_height,bg="white")
        graus_vertice_button.config(width=self.button_width,height=self.button_height,bg="white")
        sequencia_graus_grafo_button.config(width=self.button_width,height=self.button_height,bg="white")
        excentricidade_vertice_button.config(width=self.button_width,height=self.button_height,bg="white")
        distancia_caminho_minimo_button.config(width=self.button_width,height=self.button_height,bg="white")
        centralidade_proximidade_c_button.config(width=self.button_width,height=self.button_height,bg="white")

        ordem_button.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        tamanho_button.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        ordem_button.bind("<Enter>", self.button_hover)
        ordem_button.bind("<Leave>", self.button_leave)
        tamanho_button.bind("<Enter>", self.button_hover)
        tamanho_button.bind("<Leave>", self.button_leave)
        arvore_button.bind("<Enter>", self.button_hover)
        arvore_button.bind("<Leave>", self.button_leave)
        vizinhos_vertice_button.bind("<Enter>",self.button_hover)
        vizinhos_vertice_button.bind("<Leave>",self.button_leave)
        graus_vertice_button.bind("<Enter>", self.button_hover)
        graus_vertice_button.bind("<Leave>", self.button_leave)
        sequencia_graus_grafo_button.bind("<Enter>", self.button_hover)
        sequencia_graus_grafo_button.bind("<Leave>", self.button_leave)
        excentricidade_vertice_button.bind("<Enter>",self.button_hover)
        excentricidade_vertice_button.bind("<Leave>",self.button_leave)
        distancia_caminho_minimo_button.bind("<Enter>",self.button_hover)
        distancia_caminho_minimo_button.bind("<Leave>",self.button_leave)
        centralidade_proximidade_c_button.bind("<Enter>",self.button_hover)
        centralidade_proximidade_c_button.bind("<Leave>",self.button_leave)


        centro_button = tk.Button(self.frame_botao, text="Centro do Grafo", command=self.mostrar_centro_do_grafo)
        raio_button = tk.Button(self.frame_botao, text="Raio do Grafo", command=self.mostrar_raio_do_grafo)
        diametro_button = tk.Button(self.frame_botao, text="Diâmetro do Grafo", command=self.mostrar_diametro_do_grafo)

        self.configurar_fonte(arvore_button)
        self.configurar_fonte(centro_button)
        self.configurar_fonte(raio_button)
        self.configurar_fonte(diametro_button)
        self.configurar_fonte(graus_vertice_button)

        centro_button.config(width=self.button_width, height=self.button_height, bg="white")
        raio_button.config(width=self.button_width, height=self.button_height, bg="white")
        diametro_button.config(width=self.button_width, height=self.button_height, bg="white")


        centro_button.grid(row=1, column=2, padx=10, pady=10)
        raio_button.grid(row=2, column=0, padx=10, pady=10)
        diametro_button.grid(row=2, column=1, padx=10, pady=10)
        arvore_button.grid(row=3,column=3,padx=10,pady=10)
        vizinhos_vertice_button.grid(row=3,column=0,padx=10,pady=10)
        graus_vertice_button.grid(row=3,column=1,padx=10,pady=10)
        sequencia_graus_grafo_button.grid(row=2, column=2, padx=10, pady=10)
        excentricidade_vertice_button.grid(row=3,column=2,padx=10,pady=10)
        distancia_caminho_minimo_button.grid(row=1,column=3,padx=10,pady=10)
        centralidade_proximidade_c_button.grid(row=2,column=3,padx=10,pady=10)
        centro_button.bind("<Enter>", self.button_hover)
        centro_button.bind("<Leave>", self.button_leave)
        raio_button.bind("<Enter>", self.button_hover)
        raio_button.bind("<Leave>", self.button_leave)
        diametro_button.bind("<Enter>", self.button_hover)
        diametro_button.bind("<Leave>", self.button_leave)

        self.status_label = tk.Label(self.JanelaTk, text="Nenhum Grafo Carregado!", bg="white", font=(self.TipoFonte, self.TamanhoFonte,"bold"))
        self.results_label = tk.Label(self.JanelaTk, text="", bg="white", font=(self.TipoFonte, self.TamanhoFonte))
        self.results_label.place(relx=0.47, rely=0.3,anchor=tk.CENTER)
        self.status_label.place(relx=0.5, rely=0.5,anchor= tk.CENTER)

        self.set_buttons_visibility(False)

        self.JanelaTk.update_idletasks()
        screen_width = self.JanelaTk.winfo_screenwidth()
        screen_height = self.JanelaTk.winfo_screenheight()
        x = (screen_width - self.JanelaTk.winfo_width()) // 2
        y = (screen_height - self.JanelaTk.winfo_height()) // 2
        self.JanelaTk.geometry("+{}+{}".format(x, y))

        self.JanelaTk.mainloop()

    def set_buttons_visibility(self, visivel=True):
        for widget in self.frame_botao.winfo_children():
            if isinstance(widget, tk.Button):
                if visivel:
                    widget.grid()
                else:
                    widget.grid_remove()

main = Main()
