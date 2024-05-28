import os 
import time 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

from sklearn.manifold import TSNE as tsne_algorithm

class TSNE:

     def __init__(self, nome=None, base_dados=None, amostragem=None, tsne1=None, tsne2=None, dimensao=None):

        self.__verificar_extensao_csv(base_dados)
        self.__verificar_parametros(nome, base_dados, amostragem, tsne1, tsne2)

        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.tsne1 = tsne1
        self.tsne2 = tsne2
        self.dimensao = dimensao

        # Valores de pós-processamento 
        self.tempo = None 
        self.desempenho = None 
        self.variancia = None 
        self.imagem = None 

        self.__call__()

     def __call__(self):

        self.__retirar_amostragem(self.base_dados, self.amostragem)

        # Carregando arquivo CSV da amostragem e definindo vírgula como delimitador dos dados
        dataset = pd.read_csv('datasets/amostragem.csv', delimiter=",")

        # Selecionando as features e o target
        features = dataset[self.tsne1]
        target = dataset[self.tsne2]

        self.__excluir_arquivo_amostragem() 

        if self.dimensao == 2:
            inicio = time.time() # Início do processamento do TSNE
            tsne = tsne_algorithm(n_components=2)
            x_tsne = tsne.fit_transform(features)
            fim = time.time() # Fim do processamento do TSNE
            self.tempo = round(fim - inicio, 5)
            # Criando dataframe para plotar o gráfico do TSNE
            DF = pd.DataFrame(data=x_tsne, columns=["D1", "D2"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Plotando o gráfico dos dados após aplicar o TSNE
            plt.clf()
            plt.xlabel("Dimension 1", fontsize=15)
            plt.ylabel("Dimension 2",fontsize=15)
            plt.title(f"{self.nome}", fontsize=20)
            sns.scatterplot(x="D1", y="D2", hue=self.tsne2[0], data=DF_with_target, palette="Set1", legend="full", size=20)
            plt.legend(title=self.tsne2[0])

        elif self.dimensao == 3:
            inicio = time.time() # Início do processamento do TSNE
            tsne = tsne_algorithm(n_components=3)
            x_tsne = tsne.fit_transform(features)
            fim = time.time() # Fim do processamento do TSNE
            self.tempo = round(fim - inicio, 5)
            # Criando dataframe para plotar o gráfico do TSNE
            DF = pd.DataFrame(data=x_tsne, columns=["D1", "D2", "D3"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Plotando gráfico dos dados após aplicar o TSNE
            plt.clf()
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            sc = ax.scatter(DF_with_target["D1"], DF_with_target["D2"], DF_with_target["D3"], c=DF_with_target[self.tsne2[0]], cmap='viridis')
            plt.title(f"{self.nome}", fontsize=20)
            plt.colorbar(sc, ax=ax, label=self.tsne2[0])
            ax.set_xlabel('Dimension 1', fontsize=15)
            ax.set_ylabel('Dimension 2', fontsize=15)
            ax.set_zlabel('Dimension 3', fontsize=15)

        else: 
            raise ValueError('O valor informado para o parâmetro "dimensão" não é válido')

        # Salva imagem gerada pelo código
        plt.savefig(f"static/{self.nome.replace(' ', '_')}.png")
        print("Imagem gerada com sucesso.")
        self.imagem = f"{self.nome.replace(' ', '_')}.png"

     def __verificar_extensao_csv(self, file_path):
        if not file_path.endswith('.csv'):
            raise ValueError("A base de dados não é um arquivo CSV.")

     def __retirar_amostragem(self, dataset, amostragem):
          dataset_completo = pd.read_csv(dataset, delimiter=",")
          valor_amostragem = int(len(dataset_completo) * amostragem)
          amostra = dataset_completo.sample(n=valor_amostragem, random_state=42)
          amostra.to_csv('datasets/amostragem.csv', index=False)

     def __excluir_arquivo_amostragem(self):
          os.remove('datasets/amostragem.csv')

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

if __name__ == "__main__":

    mobile_price_range_2D = TSNE(
    "TSNE Price-Range 2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    ['price_range'],
    2
    )

    print(f"Tempo de processamento: {mobile_price_range_2D.tempo}")

#     mobile_price_range_3D = TSNE(
#     "TSNE Price-Range 3D",    
#     "mobile_devices.csv", 
#     1.0,
#     ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
#     ['price_range'],
#     4
#     )

#     print(f"Tempo de processamento: {mobile_price_range_3D.tempo}")