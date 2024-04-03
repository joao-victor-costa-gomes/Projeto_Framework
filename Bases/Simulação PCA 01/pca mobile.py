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
mobile_dataset = pd.read_csv("train.csv", delimiter=",")

#x = mobile_dataset.iloc[:, :-1].values # Todas as linhas e colunas com exceção da última colunas (prices)
#y = mobile_dataset.iloc[:, -1].values # Todas as linhas e a última coluna 
# Lembrando que a última coluna é a queremos destacar, que é a do preço dos celulares

# Substitua [:, :-1] por ['battery_power', 'blue', 'clock_speed', ...] 
x = mobile_dataset[['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi']].values

# Substitua [:, -1] por ['price_range']
y = mobile_dataset['price_range'].values


# Para reduzir a discrepância entre variáveis e não afetar a visualização final 
scaler_object = StandardScaler()
xTrain =  scaler_object.fit_transform(x.astype(float))
xTest = scaler_object.transform(x.astype(float))

# Pega aleatoriamente 20% das amostras para o resultado do algoritmo 
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2)

# Não aplique um PCA antes de fazer um scaler 
# Escolha de 10 colunas, a escolha vai depender do gráfico gerado
pca = decomposition.PCA(n_components=10) 
xTrain = pca.fit_transform(xTrain)
xTest = pca.transform(xTest)

model = LogisticRegression(solver="lbfgs", max_iter=1000)
start_time = time.perf_counter()
model.fit(xTrain, yTrain)
end_time = time.perf_counter()

print("Tempo de treino: ", end_time-start_time)
print("Score: ", model.score(xTest, yTest))

pca_viewer = PCA(n_components=2) 
principal_components = pca_viewer.fit_transform(xTrain)
print(pca_viewer.explained_variance_ratio_) 

# Transformar componentes principais em um dataframe para usá-los no Matplotlib  
principal_components_DF = pd.DataFrame(data=principal_components, columns=["principal component 1", "principal component 2"])

plt.figure()
plt.figure(figsize=(10, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)
plt.xlabel("Principal Component - 1", fontsize="20")
plt.ylabel("Principal Component - 2", fontsize="20")
plt.xlim(-2500, 2500)
plt.ylim(-1500, 1500)
plt.title("Principal Component Analysis - MOBILE", fontsize=20)
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
plt.show()