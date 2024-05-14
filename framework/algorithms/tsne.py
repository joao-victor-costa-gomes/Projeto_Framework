# >>>>>>>>>>>>>>>>>>>>>>>>> Consetar target
# >>>>>>>>>>>>>>>>>>>>>>>>> Definir amostragem
# >>>>>>>>>>>>>>>>>>>>>>>>> Definir tempo de processamento
# >>>>>>>>>>>>>>>>>>>>>>>>> Definir variancia
# >>>>>>>>>>>>>>>>>>>>>>>>> Definir imagem

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

from sklearn.manifold import TSNE

# # Carregando base de dados 
# dataset = pd.read_csv("datasets/mobile_devices.csv", delimiter=",")

# # Definindo as classes que quero como features
# features = ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi']
# # Definindo a classe que quero como target
# target = ["price_range"]

# x = dataset[features]
# y = dataset[target]

# tsne = TSNE(n_components=2)
# x_tsne = tsne.fit_transform(x)

# DF = pd.DataFrame(data=x_tsne, columns=["D1", "D2"])

# DF_with_target = pd.concat([DF, y], axis=1)

# plt.figure(figsize=(10, 10))
# sns.scatterplot(x="D1", y="D2", hue=target[0], data=DF_with_target, palette="Set1", legend="full")
# plt.title("t-SNE Visualization of Mobile Devices Dataset", fontsize=20)
# plt.xlabel("Dimension 1", fontsize=15)
# plt.ylabel("Dimension 2", fontsize=15)
# plt.legend(title=target[0])
# plt.show()

class TSNE_2D:

     def __init__(self, nome=None, base_dados=None, amostragem=None, tsne1=None, tsne2=None):

        self.__verificar_extensao_csv(base_dados)
        self.__verificar_parametros(nome, base_dados, amostragem, tsne1, tsne2)

        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.tsne1 = tsne1
        self.tsne2 = tsne2

        # Valores de pós-processamento 
        self.tempo = None 
        self.desempenho = None 
        self.variancia = None 
        self.imagem = None 

     def __call__(self):
        # Carregando arquivos CSV e definindo vírgula como delimitador dos dados
        dataset = pd.read_csv(self.base_dados, delimiter=",")

        # Selecionando as features e o target
        features = dataset[self.tsne1].values 
        target = dataset[self.tsne2].values

        # Aplicando o TSNE (duas dimensões)
        tsne = TSNE(n_components=2)
        x_tsne = tsne.fit_transform(features)

        # Criando dataframe para plotar o gráfico do TSNE
        DF = pd.DataFrame(data=x_tsne, columns=["D1", "D2"])
        DF_with_target = pd.concat([DF, target], axis=1)

        # Plotando gráfico dos dados após aplicar o TSNE
        plt.figure(figsize=(10, 10))
        plt.xlabel("Dimension 1", fontsize=20)
        plt.ylabel("Dimension 2",fontsize=20)
        plt.title(f"{self.nome}", fontsize=20)
        sns.scatterplot(x="D1", y="D2", hue=target[0], data=DF_with_target, palette="Set1", legend="full")
        plt.legend(title=target[0])
        plt.show()

    # Verifica se a base de dados enviada pelo usuário é um arquivo .csv
     def __verificar_extensao_csv(self, file_path):
        if not file_path.endswith('.csv'):
            raise ValueError("A base de dados não é um arquivo CSV.")

    # Verifica se tem algum parâmetro que falta ser informado
     def __verificar_parametros(self, nome, base_dados, amostragem, tsne1, tsne2):
        if nome == None:
             raise ValueError('Faltou informar o parâmetro "nome"')
        if base_dados == None:
             raise ValueError('Faltou informar o parâmetro "base_dados"')
        if amostragem == None:
             raise ValueError('Faltou informar o parâmetro "amostragem"')
        if tsne1 == None:
             raise ValueError('Faltou informar o parâmetro "tsne1"')
        if tsne2 == None:
             raise ValueError('Faltou informar o parâmetro "tsne2"')
        

mobile = TSNE_2D(
    "PCA Mobile Devices - Price Range",
    "mobile_devices.csv", 
    0.2,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    ['price_range']
)

mobile()
