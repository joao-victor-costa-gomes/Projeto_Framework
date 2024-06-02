import os 
import time 
import pandas as pd
import plotly.express as px

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

        features = dataset[self.tsne1] # Valores que serão usados na construção do gráfico
        target = dataset[self.tsne2].astype(str) # Valores que serão plotados como pontos no gráfico 

        self.__excluir_arquivo_amostragem()

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
            figure.write_html(f"static/{self.nome.replace(' ', '_')}.html")
            print("Gráfico gerado com sucesso")
            self.imagem = f"{self.nome.replace(' ', '_')}.html"

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
            figure.write_html(f"static/{self.nome.replace(' ', '_')}.html")
            print("Gráfico gerado com sucesso")
            self.imagem = f"{self.nome.replace(' ', '_')}.html"

        else:
            raise ValueError('O valor do parâmetro "dimensao" só pode ser 2 ou 3')

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

    mobile_price_range = TSNE(
    "TSNE-Wifi-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    ['price_range'],
    2
    )

    print(f"Tempo de processamento: {mobile_price_range.tempo}")
