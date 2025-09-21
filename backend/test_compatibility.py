import numpy as np
import matplotlib.pyplot as plt
import scipy
import plotly
import flask

print("✅ Todas las librerías importadas correctamente")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"SciPy: {scipy.__version__}")
print(f"Plotly: {plotly.__version__}")
print(f"Flask: {flask.__version__}")

# Test básico de NumPy 2.x
arr = np.array([1, 2, 3])
print(f"Array test: {arr}")
print("✅ NumPy 2.x funciona correctamente")