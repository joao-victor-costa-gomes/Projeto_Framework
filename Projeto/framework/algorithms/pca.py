import os 
import numpy 
import pandas

import time 

import matplotlib.pyplot as plt 

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

class PCA_2D:

    def __init__(self, nome=None, base_dados=None, amostragem=None, pc1=None, pc2=None):

        if nome == None or base_dados == None or amostragem == None or pc1 == None or pc2 == None:
            raise ValueError("Faltou informar algum padrão obrigatório na função PCA_2D")

        if not self.verificar_extensao_csv(base_dados):
            raise ValueError("O arquivo enviado não é um arquivo CSV")

        # Valores de pré-processamento 
        self.nome = nome.replace(' ', '_')
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.pc1 = pc1
        self.pc2 = pc2
        
        # Valores de pós-processamento 
        self.tempo = None 
        self.desempenho = None 
        self.variancia = None 
        self.imagem = None 

        # Remove a necessidade de precisar executar a instância
        self.__call__()

        # Remove o "dataset/" do nome da base dados 
        self.base_dados = base_dados 

    def __call__(self):
        # Carregando arquivos CSV e definindo vírgula como delimitador
        dataset = pandas.read_csv(self.base_dados, delimiter=",")

        # Selecionando o componente principal 1 e o componente principal 2
        x = dataset[self.pc1].values 
        y = dataset[self.pc2].values

        # Reduzindo discrepância das variáveis 
        scaler = StandardScaler()
        xTrain = scaler.fit_transform(x.astype(float))
        xTest = scaler.fit_transform(x.astype(float))

        # Pegando aleatoriamente a % informada de amostras 
        xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=self.amostragem)

        # Aplicando algoritmo do PCA
        pca = PCA(n_components=2)
        xTrain = pca.fit_transform(xTrain)
        xTest = pca.transform(xTest)

        self.variancia = pca.explained_variance_ratio_

        # Calculando tempo de treino e desempenho do algoritmo 
        model = LogisticRegression(solver="lbfgs", max_iter=1000)
        start_time = time.perf_counter()
        model.fit(xTrain, yTrain)
        end_time = time.perf_counter()

        self.tempo = end_time - start_time

        self.desempenho = model.score(xTest, yTest)

        # Transformar componentes principais em um dataframe para usá-los no Matplotlib  
        principal_components_DF = pandas.DataFrame(data=xTrain, columns=["principal component 1", "principal component 2"])

        # Construindo figura que será exibida
        plt.figure()
        plt.figure(figsize=(10, 10))
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.xlabel("Principal Component - 1", fontsize="12")
        plt.ylabel("Principal Component - 2", fontsize="12")
        plt.xlim(-2500, 2500)
        plt.ylim(-1500, 1500)
        plt.title(f"{self.nome}", fontsize=20)
        targets = [0, 1, 2, 3]
        colors = ["r", "g", "b", "y"]

        for target, color in zip(targets, colors):
            indicesToKeep = yTrain == target 
            plt.scatter(principal_components_DF.loc[indicesToKeep, "principal component 1"], 
                        principal_components_DF.loc[indicesToKeep, "principal component 2"], 
                        c = color,
                        s = 25,
                        alpha = 0.5   
            )

        plt.legend(targets, prop={"size":15})
        plt.savefig(f"static/{self.nome}.png")
        self.imagem = f"{self.nome}.png"

    # Verifica se a base de dados enviada pelo usuário é um arquivo .csv
    def verificar_extensao_csv(self, base_dados):
        _, extensao = os.path.splitext(base_dados)
        return extensao.lower() == '.csv'



        
