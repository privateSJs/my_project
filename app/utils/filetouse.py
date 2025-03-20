import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Użycie numpy
a = np.array([1, 2, 3])
b = np.dot(a, a)  # Mnożenie macierzowe
c = np.mean(a)  # Średnia

# Użycie pandas
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
df_mean = df.mean()  # Obliczanie średniej w pandas

# Użycie TensorFlow
tensor = tf.constant([[1, 2], [3, 4]])
tensor_squared = tf.square(tensor)  # Podnoszenie do kwadratu

# Użycie Matplotlib
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Testowy wykres")

# Użycie Scikit-Learn
model = LinearRegression()
model.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])  # Dopasowanie modelu regresji liniowej
