# Importando uma base de dados que já vem na biblioteca sklearn
from sklearn.datasets import load_breast_cancer

# Importando a biblioteca numpy ara remodelar os dados de breast_data e breast_labels 
import numpy as np 

# Importando a biblioteca pandas para criar um DataFrame
import pandas as pd 

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt 

cancer = load_breast_cancer() # Carrega a base de dados da biblioteca 

cancer_data = cancer.data  # Atribuição da data da base de dados
cancer_feature_names = cancer.feature_names # Atribuição do nome das colunas 

# Criando um DataFrame para usá-lo no Matplotlib  
cancer_dataframe = pd.DataFrame(cancer_data, columns=cancer_feature_names)

# Valores com grandes diferenças podem afetar o resultado final do PCA
# Para isso, o scaler serve para "reduzir" essas discrepâncias 
scaler_object = StandardScaler()
scaler_object.fit(cancer_dataframe)

scaled_data = scaler_object.transform(cancer_dataframe)

pca = PCA(n_components=2)
pca.fit(scaled_data)

x_pca = pca.transform(scaled_data)

plt.figure(figsize=(8, 6))
plt.scatter(x_pca[:, 0], x_pca[:, 1], c=cancer['target'])
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

plt.savefig('pca_breast_cancer.png')
plt.show()




