import numpy 
import pandas

import time 

import matplotlib.pyplot as plt 

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

class PCA_2D:

    '''O algoritmo será uma classe que será importada pelo usuário e reberá uma base de dados e outros parâmetros. Minha ideia inicial para as variáveis necessárias são: base de dados, amostragem, dimensão, coluna 1 2 e 3, componente 1 2 e 3. Para os atributos dessa classe: tempo de processamento, precisão, local da imagem'''

    def __init__(self, nome, base_dados, amostragem, pc1, pc2):
        self.nome = nome
        self.base_dados = base_dados
        self.amostragem = amostragem
        self.pc1 = pc1
        self.pc2 = pc2
        
        self.tempo = None 
        self.desempenho = None 
        self.variancia = None 
        self.imagem = None 

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
        print(f'Variância: {self.variancia}')

        # Vendo tempo de treino do algoritmo 
        model = LogisticRegression(solver="lbfgs", max_iter=1000)
        start_time = time.perf_counter()
        model.fit(xTrain, yTrain)
        end_time = time.perf_counter()

        self.tempo = end_time - start_time
        print(f"Tempo: {self.tempo}")

        self.desempenho = model.score(xTest, yTest)
        print(f"Desempenho: {self.desempenho}")

        # Transformar componentes principais em um dataframe para usá-los no Matplotlib  
        principal_components_DF = pandas.DataFrame(data=xTrain, columns=["principal component 1", "principal component 2"])

        # Construindo figura que será exibida
        plt.figure()
        plt.figure(figsize=(10, 10))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=14)
        plt.xlabel("Principal Component - 1", fontsize="20")
        plt.ylabel("Principal Component - 2", fontsize="20")
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
        # plt.show()
        plt.savefig(f"static/{self.nome}.png")
        self.imagem = f"{self.nome}.png"


        
