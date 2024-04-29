import numpy as np 
import pandas as pd 
import time 

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import decomposition
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt 

# Carrega arquivo de dados csv e indica que seus dados estão delimitiamdos por vírgula 
stellar_dataset = pd.read_csv("datasets/star_classification.csv", delimiter=",") # <----- VARIÁVEL

# O eixo X representa todos os valores que não estão na coluna "class"
x = stellar_dataset.loc[:, stellar_dataset.columns != "class"].values 

# O eixo Y representa os valores da coluna "class"
# Possíveis valores da coluna: GALAXY, QSO, STAR 
y = stellar_dataset["class"].values 

# GALAXY, QSO e STAR não são valores propícios para usar no algoritmo 
# Por isso a função LabelEncoder() converte eles em 0, 1 e 2
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)

# Valores com grandes diferenças podem afetar o resultado final do PCA
# Para isso, essa parte serve para "reduzir" essas discrepâncias 
scale_object = StandardScaler()
x = scale_object.fit_transform(x.astype(float))

# Pega aleatoriamente 15% das amostras para o resultado do algoritmo 
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.15) # <----- VARIÁVEL

# Não aplique um PCA antes de fazer um scaler 
pca = decomposition.PCA(n_components=2) # Escolha de 10 colunas, a escolha vai depender do gráfico gerado
xTrain = pca.fit_transform(xTrain)
xTest = pca.transform(xTest)

model = LogisticRegression(solver="lbfgs", max_iter=400)
start_time = time.perf_counter()
model.fit(xTrain, yTrain)
end_time = time.perf_counter()
print("Tempo de treino: ", end_time-start_time) # <----- ATRIBUTO
print("Score: ", model.score(xTest, yTest))     # <----- ATRIBUTO
 
pca_viewer = PCA(n_components=2) # PARA representação 2D <----- VARIÁVEL
principal_components = pca_viewer.fit_transform(xTrain)
print(pca_viewer.explained_variance_ratio_) # A soma dos dois eixos explica a precisão do PCA (vendo em %)

# Transformar componentes principais em um dataframe para usá-los no Matplotlib  
principal_components_DF = pd.DataFrame(data=principal_components, columns=["principal component 1", "principal component 2"])

yTrain.astype(int) # Converter as colunas para inteiro
yTrain = np.where(yTrain == "0", "GALAXY", yTrain)
yTrain = np.where(yTrain == "1", "QSO", yTrain) # Serve para desfazer o LabelEncoder()
yTrain = np.where(yTrain == "2", "STAR", yTrain)

plt.figure()
plt.figure(figsize=(10, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)
plt.xlabel("Principal Component - 1", fontsize="20")
plt.ylabel("Principal Component - 2", fontsize="20")
plt.xlim(-10, 10)
plt.ylim(-1, 1)
plt.title("Principal Component Analysis - Stellar", fontsize=20)
targets = ["GALAXY", "QSO", "STAR"]
colors = ["r", "g", "b"]

for target, color in zip(targets, colors):
    indicesToKeep = yTrain == target 
    plt.scatter(principal_components_DF.loc[indicesToKeep, "principal component 1"], 
                principal_components_DF.loc[indicesToKeep, "principal component 2"], 
                c = color,
                s = 25,
                alpha = 0.5   
    )

plt.legend(targets, prop={"size":15})
plt.show()