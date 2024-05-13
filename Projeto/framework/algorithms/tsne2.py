import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

import seaborn as sns

# Carregando base de dados 
dataset = pd.read_csv("datasets/mobile_devices.csv", delimiter=",")

# Definindo as classes que quero como features
features = ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', "price_range"]
# Definindo a classe que quero como target
target = ['wifi']

x = dataset[features]
y = dataset[target]

tsne = TSNE(n_components=2, n_iter=500)
x_tsne = tsne.fit_transform(x)

DF = pd.DataFrame(data=x_tsne, columns=["D1", "D2"])

DF_with_target = pd.concat([DF, y], axis=1)

plt.figure(figsize=(10, 8))
sns.scatterplot(x="D1", y="D2", hue="wifi", data=DF_with_target, palette="Set1", legend="full")
plt.title("t-SNE Visualization of Mobile Devices Dataset")
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.legend(title="Price Range")
plt.savefig("static/mobile-wifi.png")
plt.show()
