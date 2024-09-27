import os 
import time 
import utils
import pandas as pd
import plotly.express as px

from sklearn.decomposition import KernelPCA as kpca_algorithm
from sklearn.preprocessing import StandardScaler

class KPCA:
    def __init__(self, nome=None, base_dados=None, amostragem=None, kpca1=None, kpca2=None, dimensao=None, tipo_imagem=None, standardscaler=False):

        utils.verificar_extensao_csv(base_dados)
        utils.verificar_parametros(nome, base_dados, amostragem, kpca1, kpca2, tipo_imagem)

        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.kpca1 = kpca1
        self.kpca2 = kpca2
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

        features = dataset[self.kpca1] # Valores que serão usados na construção do gráfico
        target = dataset[self.kpca2].astype(str) # Valores que serão plotados como pontos no gráfico 

        utils.excluir_arquivo_amostragem()

        if self.standardscaler:
            scaler = StandardScaler()
            features = scaler.fit_transform(features)

        # Processando gráfico 2D
        if self.dimensao == 2:
            inicio = time.time() # Início do processamento do KPCA
            kpca = kpca_algorithm(n_components=2, kernel='poly')
            x_kpca = kpca.fit_transform(features)
            fim = time.time() # Fim do processamento do KPCA
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            # total_var = kpca.explained_variance_ratio_.sum() * 100
            # self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do kpca
            DF = pd.DataFrame(data=x_kpca, columns=["KPCA1", "KPCA2"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o kpca
            figure = px.scatter(DF_with_target, x="KPCA1", y="KPCA2", title=self.nome, color=self.kpca2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            self.imagem = utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        # Processando gráfico 3D
        elif self.dimensao == 3:
            inicio = time.time() # Início do processamento do KPCA
            kpca = kpca_algorithm(n_components=3)
            x_kpca = kpca.fit_transform(features)
            fim = time.time() # Fim do processamento do KPCA
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            # total_var = kpca.explained_variance_ratio_.sum() * 100
            # self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do KPCA
            DF = pd.DataFrame(data=x_kpca, columns=["KPCA1", "KPCA2", "KPCA3"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o kpca
            figure = px.scatter_3d(DF_with_target, x="KPCA1", y="KPCA2", z="KPCA3", title=self.nome, color=self.kpca2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            self.imagem = utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        else:
            raise ValueError('O valor do parâmetro "dimensao" só pode ser 2 ou 3')


# Testando funcionamento do algoritmo 
if __name__ == "__main__":
    
    # Versão HTML
    mobile1 = KPCA(
    "KPCA-MOBILE-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi'],
    ['price_range'],
    2,
    'html',
    False
    )
    print(f"Tempo de processamento (KPCA Interativo): {mobile1.tempo}")
    print(f"Variância total: {mobile1.variancia}")

    # Versão PNG
    mobile2 = KPCA(
    "KPCA-MOBILE-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi'],
    ['price_range'],
    2,
    'png',
    False
    )
    print(f"Tempo de processamento (KPCA Imagem): {mobile2.tempo}")
    print(f"Variância total: {mobile2.variancia}")

