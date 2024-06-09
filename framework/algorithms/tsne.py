import os 
import time 
import utils
import pandas as pd
import plotly.express as px

from sklearn.manifold import TSNE as tsne_algorithm

class TSNE:
    def __init__(self, nome=None, base_dados=None, amostragem=None, tsne1=None, tsne2=None, dimensao=None, tipo_imagem=None):

        utils.verificar_extensao_csv(base_dados)
        utils.verificar_parametros(nome, base_dados, amostragem, tsne1, tsne2, tipo_imagem)

        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.tsne1 = tsne1
        self.tsne2 = tsne2
        self.dimensao = dimensao
        self.tipo_imagem = tipo_imagem

        # Valores de pós-processamento 
        self.tempo = None 
        self.desempenho = None 
        self.variancia = None 
        self.imagem = None 

        self.__call__()

    def __call__(self):

        utils.retirar_amostragem(self.base_dados, self.amostragem)

        # Carregando arquivo CSV da amostragem e definindo vírgula como delimitador dos dados
        dataset = pd.read_csv('datasets/amostragem.csv', delimiter=",")

        features = dataset[self.tsne1] # Valores que serão usados na construção do gráfico
        target = dataset[self.tsne2].astype(str) # Valores que serão plotados como pontos no gráfico 

        utils.excluir_arquivo_amostragem()

        # Processando gráfico 2D
        if self.dimensao == 2:
            inicio = time.time() # Início do processamento do T-SNE
            tsne = tsne_algorithm(n_components=2)
            x_tsne = tsne.fit_transform(features)
            fim = time.time() # Fim do processamento do T-SNE
            self.tempo = round(fim - inicio, 5)
            # Criando DataFrame para plotar o gráfico do T-SNE
            DF = pd.DataFrame(data=x_tsne, columns=["TSNE1", "TSNE2"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o T-SNE
            figure = px.scatter(DF_with_target, x="TSNE1", y="TSNE2", title=self.nome, color=self.tsne2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        # Processando gráfico 3D
        elif self.dimensao == 3:
            inicio = time.time() # Início do processamento do T-SNE
            tsne = tsne_algorithm(n_components=3)
            x_tsne = tsne.fit_transform(features)
            fim = time.time() # Fim do processamento do T-SNE
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            total_var = ""
            self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do T-SNE
            DF = pd.DataFrame(data=x_tsne, columns=["TSNE1", "TSNE2", "TSNE3"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o T-SNE
            figure = px.scatter_3d(DF_with_target, x="TSNE1", y="TSNE2", z="TSNE3", title=self.nome, color=self.tsne2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        else:
            raise ValueError('O valor do parâmetro "dimensao" só pode ser 2 ou 3')


# Testando funcionamento do algoritmo 
if __name__ == "__main__":
    mobile_price_range = TSNE(
    "TSNE-Price_Range-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    None,
    2,
    'html'
    )
    print(f"Tempo de processamento: {mobile_price_range.tempo}")