from mpl_toolkits.mplot3d import Axes3D
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
features = ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi']
# Definindo a classe que quero como target
target = ["price_range"]

x = dataset[features]
y = dataset[target]

# t-SNE with 3 components
tsne_3d = TSNE(n_components=3, n_iter=500)
x_tsne_3d = tsne_3d.fit_transform(x)

# Creating DataFrame with 3D t-SNE data
DF_3d = pd.DataFrame(data=x_tsne_3d, columns=["D1", "D2", "D3"])
DF_3d_with_target = pd.concat([DF_3d, y], axis=1)

# Plotting 3D t-SNE data
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
scatter = ax.scatter(DF_3d_with_target["D1"], DF_3d_with_target["D2"], DF_3d_with_target["D3"],
                     c=DF_3d_with_target["price_range"], cmap='Set1')

# Legend
legend = ax.legend(*scatter.legend_elements(), title="Price Range")
ax.add_artist(legend)

# Axes labels
ax.set_xlabel('Dimension 1')
ax.set_ylabel('Dimension 2')
ax.set_zlabel('Dimension 3')

# Title
plt.title("t-SNE 3D Visualization of Mobile Devices Dataset")

plt.show()
