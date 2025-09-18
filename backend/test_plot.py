# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.graphic_method import LinearProgrammingProblem

# Probar con un problema de ejemplo
problem = LinearProgrammingProblem(
    "Maximizar 3x + 2y",
    ["2x + y <= 100", "x + y <= 80", "x >= 0", "y >= 0"]
)

result = problem.solve_with_plot()

print("Punto óptimo:", result["optimal_point"])
print("Valor óptimo:", result["optimal_value"])
print("Gráfico generado:", "plot" in result and result["plot"] is not None)

# Guardar gráfico para verlo
if "plot" in result and result["plot"]:
    import base64
    with open("test_plot.png", "wb") as f:
        f.write(base64.b64decode(result["plot"]))
    print("Gráfico guardado como test_plot.png")