import os 
import time 
import utils
import pandas as pd
import plotly.express as px

import umap.umap_ as umap 
from sklearn.preprocessing import StandardScaler

class UMAP:
    def __init__(self, nome=None, base_dados=None, amostragem=None, umap1=None, umap2=None, dimensao=None, tipo_imagem=None, standardscaler=False):

        utils.verificar_extensao_csv(base_dados)
        utils.verificar_parametros(nome, base_dados, amostragem, umap1, umap2, tipo_imagem)

        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.umap1 = umap1
        self.umap2 = umap2
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

        features = dataset[self.umap1] # Valores que serão usados na construção do gráfico
        target = dataset[self.umap2].astype(str) # Valores que serão plotados como pontos no gráfico 

        utils.excluir_arquivo_amostragem()

        if self.standardscaler:
            scaler = StandardScaler()
            features = scaler.fit_transform(features)

        # Processando gráfico 2D  y=target.values.ravel())
        if self.dimensao == 2:
            inicio = time.time() # Início do processamento do UMAP
            reducer = umap.UMAP(n_components=2)
            x_umap = reducer.fit_transform(features)
            fim = time.time() # Fim do processamento do UMAP
            self.tempo = round(fim - inicio, 5)
            # Criando DataFrame para plotar o gráfico do UMAP
            DF = pd.DataFrame(data=x_umap, columns=["UMAP1", "UMAP2"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o UMAP
            figure = px.scatter(DF_with_target, x="UMAP1", y="UMAP2", title=self.nome, color=self.umap2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            self.imagem = utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        # Processando gráfico 3D
        elif self.dimensao == 3:
            inicio = time.time() # Início do processamento do UMAP
            reducer = umap.UMAP(n_components=3)
            x_umap = reducer.fit_transform(features)
            fim = time.time() # Fim do processamento do UMAP
            self.tempo = round(fim - inicio, 5)
            # Criando DataFrame para plotar o gráfico do UMAP
            DF = pd.DataFrame(data=x_umap, columns=["UMAP1", "UMAP2", "UMAP3"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o UMAP
            figure = px.scatter_3d(DF_with_target, x="UMAP1", y="UMAP2", z="UMAP3", title=self.nome, color=self.umap2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            self.imagem = utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        else:
            raise ValueError('O valor do parâmetro "dimensao" só pode ser 2 ou 3')


# Testando funcionamento do algoritmo 
if __name__ == "__main__":
    
    # Versão HTML
    mobile1 = UMAP(
    "UMAP-MOBILE-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi'],
    ['price_range'],
    2,
    'html',
    False
    )
    print(f"Tempo de processamento (UMAP Interativo): {mobile1.tempo}")

    # Versão PNG
    mobile2 = UMAP(
    "UMAP-MOBILE-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi'],
    ['price_range'],
    2,
    'png',
    False
    )
    print(f"Tempo de processamento (UMAP Imagem): {mobile2.tempo}")
