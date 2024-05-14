import os 
import numpy as np
import pandas
import seaborn

import time 

import matplotlib.pyplot as plt 

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

class PCA_2D:

    def __init__(self, nome=None, base_dados=None, amostragem=None, pc1=None, pc2=None):

        if nome == None or base_dados == None or amostragem == None or pc1 == None or pc2 == None:
            raise ValueError("Faltou informar algum dos parâmetros obrigatórios na função PCA_2D")

        if not self.verificar_extensao_csv(base_dados):
            raise ValueError("O arquivo enviado não é um arquivo CSV")

        # Valores de pré-processamento 
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.pc1 = pc1
        self.pc2 = pc2
        
        # Valores de pós-processamento 
        self.tempo = None 
        self.desempenho = None 
        self.variancia = None 
        self.imagem = None 

        # Executa já na construção
        self.__call__()

    def __call__(self):
        # Carregando arquivos CSV e definindo vírgula como delimitador
        dataset = pandas.read_csv(self.base_dados, delimiter=",")

        dataset_amostragem = dataset.sample(frac=0.5, random_state=42)

        # Selecionando o componente principal 1 e o componente principal 2
        x = dataset_amostragem[self.pc1].values 
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
        plt.xlabel("Principal Component - 1", fontsize="20")
        plt.ylabel("Principal Component - 2", fontsize="20")
        #plt.xlim(-2500, 2500)
        #plt.ylim(-2500, 2500)
        plt.title(f"{self.nome}", fontsize=20)
        targets = self.pegar_targets(dataset, self.pc2)

        seaborn.set_palette("Set1")
        colors = seaborn.color_palette(n_colors=len(targets))

        for target, color in zip(targets, colors):
            indicesToKeep = yTrain == target 
            plt.scatter(principal_components_DF.loc[indicesToKeep, "principal component 1"], 
                        principal_components_DF.loc[indicesToKeep, "principal component 2"], 
                        c=[colors[targets.index(target)]],
                        s = 25,
                        alpha = 0.5   
            )

        plt.legend(targets, prop={"size":15})

        # Salva imagem gerada pelo código
        plt.savefig(f"static/{self.nome.replace(' ', '_')}.png")
        self.imagem = f"{self.nome.replace(' ', '_')}.png"

    # Verifica se a base de dados enviada pelo usuário é um arquivo .csv
    def verificar_extensao_csv(self, base_dados):
        _, extensao = os.path.splitext(base_dados)
        return extensao.lower() == '.csv'

    # Pegar automaticamente os targets sem precisar informar
    def pegar_targets(self, dataframe, column_name):
        targets = dataframe[column_name].unique().tolist()
        return targets

    
    # Aplicar LabelEncoder nas colunas com dados do tipo texto
    def aplicar_label_encoder(self, dataset):
        colunas_string = []

        for coluna in dataset.columns:
            if dataset[coluna].dtype == 'object':
                colunas_string.append(coluna)

        labelencoder = LabelEncoder()

        for coluna in colunas_string:
            dataset[coluna] = labelencoder.fit_transform(dataset[coluna])



if __name__ == "__main__":
    # star = PCA_2D(
    # "PCA Star Classification",
    # "star_classification.csv", 
    # 0.2,
    # ['obj_ID','alpha','delta','u','g','r','i','z','run_ID','rerun_ID','cam_col','field_ID','spec_obj_ID','class','redshift','plate','MJD','fiber_ID'],
    # 'class'
    # )

    mobile = PCA_2D(
    "PCA Mobile Devices",
    "mobile_devices.csv", 
    0.2,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    'price_range'
    )