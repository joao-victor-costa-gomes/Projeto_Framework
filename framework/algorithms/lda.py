import os 
import time 
import utils
import pandas as pd
import plotly.express as px

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda_algorithm

class LDA:
    def __init__(self, nome=None, base_dados=None, amostragem=None, lda1=None, lda2=None, dimensao=None, tipo_imagem=None):

        utils.verificar_extensao_csv(base_dados)
        utils.verificar_parametros(nome, base_dados, amostragem, lda1, lda2, tipo_imagem)

        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.lda1 = lda1
        self.lda2 = lda2
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

        features = dataset[self.lda1] # Valores que serão usados na construção do gráfico
        target = dataset[self.lda2].astype(str) # Valores que serão plotados como pontos no gráfico 

        utils.excluir_arquivo_amostragem()

        # Processando gráfico 2D
        if self.dimensao == 2:
            inicio = time.time() # Início do processamento do LDA
            lda = lda_algorithm(n_components=2)
            x_lda = lda.fit_transform(X=features, y=target)
            fim = time.time() # Fim do processamento do LDA
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            total_var = lda.explained_variance_ratio_.sum() * 100
            self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do LDA
            DF = pd.DataFrame(data=x_lda, columns=["LDA1", "LDA2"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o LDA
            figure = px.scatter(DF_with_target, x="LDA1", y="LDA2", title=self.nome, color=self.lda2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

        # Processando gráfico 3D
        elif self.dimensao == 3:
            inicio = time.time() # Início do processamento do LDA
            lda = lda_algorithm(n_components=3)
            x_lda = lda.fit_transform(X=features, y=target)
            fim = time.time() # Fim do processamento do LDA
            self.tempo = round(fim - inicio, 5)
            # Calculando variância dos dados
            total_var = lda.explained_variance_ratio_.sum() * 100
            self.variancia = total_var
            # Criando DataFrame para plotar o gráfico do LDA
            DF = pd.DataFrame(data=x_lda, columns=["LDA1", "LDA2", "LDA3"])
            DF_with_target = pd.concat([DF, target], axis=1)
            # Criando o gráfico com os dados após aplicar o LDA
            figure = px.scatter_3d(DF_with_target, x="LDA1", y="LDA2", z="LDA3", title=self.nome, color=self.lda2[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            figure.write_html(f"static/{self.nome.replace(' ', '_')}.html")
            print("Gráfico gerado com sucesso")
            self.imagem = f"{self.nome.replace(' ', '_')}.html"

        else:
            raise ValueError('O valor do parâmetro "dimensao" só pode ser 2 ou 3')


# Testando funcionamento do algoritmo 
if __name__ == "__main__":
    mobile_price_range = LDA(
    "LDA-PriceRange-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    ['price_range'],
    2,
    "html"
    )
    print(f"Tempo de processamento: {mobile_price_range.tempo}")
    print(f"Variância total: {mobile_price_range.variancia}")