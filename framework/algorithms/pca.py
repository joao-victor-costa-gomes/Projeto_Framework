import os 
import time 
import utils
import pandas as pd
import plotly.express as px

from sklearn.decomposition import PCA as pca_algorithm
from sklearn.preprocessing import StandardScaler

class PCA:
    def __init__(self, nome=None, base_dados=None, amostragem=None, pca1=None, pca2=None, dimensao=None, tipo_imagem=None, standardscaler=False):

        utils.verificar_extensao_csv(base_dados)
        utils.verificar_parametros(nome, base_dados, amostragem, pca1, pca2, tipo_imagem)

        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.pca1 = pca1
        self.pca2 = pca2
        self.dimensao = dimensao
        self.tipo_imagem = tipo_imagem
        self.standardscaler = standardscaler

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

        features = dataset[self.pca1] # Valores que serão usados na construção do gráfico
        target = dataset[self.pca2].astype(str) # Valores que serão plotados como pontos no gráfico 

        utils.excluir_arquivo_amostragem()

        if self.standardscaler:
            scaler = StandardScaler()
            features = scaler.fit_transform(features)

        # Processando gráfico 2D
        if self.dimensao == 2:
            inicio = time.time() # Início do processamento do PCA
            pca = pca_algorithm(n_components=2)
            x_pca = pca.fit_transform(features)
            fim = time.time() # Fim do processamento do PCA
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            total_var = pca.explained_variance_ratio_.sum() * 100
            self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do PCA
            DF = pd.DataFrame(data=x_pca, columns=["PCA1", "PCA2"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o PCA
            figure = px.scatter(DF_with_target, x="PCA1", y="PCA2", title=self.nome, color=self.pca2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        # Processando gráfico 3D
        elif self.dimensao == 3:
            inicio = time.time() # Início do processamento do PCA
            pca = pca_algorithm(n_components=3)
            x_pca = pca.fit_transform(features)
            fim = time.time() # Fim do processamento do PCA
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            total_var = pca.explained_variance_ratio_.sum() * 100
            self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do PCA
            DF = pd.DataFrame(data=x_pca, columns=["PCA1", "PCA2", "PCA3"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o PCA
            figure = px.scatter_3d(DF_with_target, x="PCA1", y="PCA2", z="PCA3", title=self.nome, color=self.pca2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        else:
            raise ValueError('O valor do parâmetro "dimensao" só pode ser 2 ou 3')


# Testando funcionamento do algoritmo 
if __name__ == "__main__":
    mobile_price_range = PCA(
    "PCA-PriceRange-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    ['price_range'],
    2, 
    "html")
    print(f"Tempo de processamento: {mobile_price_range.tempo}")
    print(f"Variância total: {mobile_price_range.variancia}")