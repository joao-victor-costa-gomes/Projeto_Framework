import os 
import time 
import utils
import pandas as pd
import plotly.express as px

from sklearn.manifold import LocallyLinearEmbedding as lle_algorithm
from sklearn.preprocessing import StandardScaler

class LLE:
    def __init__(self, nome=None, base_dados=None, amostragem=None, lle1=None, lle2=None, dimensao=None, tipo_imagem=None, standardscaler=False):

        utils.verificar_extensao_csv(base_dados)
        utils.verificar_parametros(nome, base_dados, amostragem, lle1, lle2, tipo_imagem)

        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.lle1 = lle1
        self.lle2 = lle2
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

        features = dataset[self.lle1] # Valores que serão usados na construção do gráfico
        target = dataset[self.lle2].astype(str) # Valores que serão plotados como pontos no gráfico 

        utils.excluir_arquivo_amostragem()

        if self.standardscaler:
            scaler = StandardScaler()
            features = scaler.fit_transform(features)

        # Processando gráfico 2D
        if self.dimensao == 2:
            inicio = time.time() # Início do processamento do LLE
            lle = lle_algorithm(n_components=2)
            x_lle = lle.fit_transform(features)
            fim = time.time() # Fim do processamento do LLE
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            # total_var = lle.explained_variance_ratio_.sum() * 100
            # self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do LLE
            DF = pd.DataFrame(data=x_lle, columns=["LLE1", "LLE2"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o LLE
            figure = px.scatter(DF_with_target, x="LLE1", y="LLE2", title=self.nome, color=self.lle2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            self.imagem = utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        # Processando gráfico 3D
        elif self.dimensao == 3:
            inicio = time.time() # Início do processamento do LLE
            lle = lle_algorithm(n_components=3)
            x_lle = lle.fit_transform(features)
            fim = time.time() # Fim do processamento do LLE
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            # total_var = lle.explained_variance_ratio_.sum() * 100
            # self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do LLE
            DF = pd.DataFrame(data=x_lle, columns=["LLE1", "LLE2", "LLE3"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o LLE
            figure = px.scatter_3d(DF_with_target, x="LLE1", y="LLE2", z="LLE3", title=self.nome, color=self.lle2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            self.imagem = utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        else:
            raise ValueError('O valor do parâmetro "dimensao" só pode ser 2 ou 3')


# Testando funcionamento do algoritmo 
if __name__ == "__main__":
    
    # Versão HTML
    mobile1 = LLE(
    "LLE-MOBILE-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi'],
    ['price_range'],
    2,
    'html',
    True
    )
    print(f"Tempo de processamento (LLE Interativo): {mobile1.tempo}")
    print(f"Variância total: {mobile1.variancia}")

    # Versão PNG
    mobile2 = LLE(
    "LLE-MOBILE-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi'],
    ['price_range'],
    2,
    'png',
    True 
    )
    print(f"Tempo de processamento (LLE Imagem): {mobile2.tempo}")
    print(f"Variância total: {mobile2.variancia}")

