# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.plotly_graphics import InteractiveLinearProgramming

# Problema con región factible compleja
problem = InteractiveLinearProgramming(
    "maximize 300x + 100y",
    [
        "40x + 8y <=800", 
        "10x + 5y <=320",
        "x>=0",
        "y>=0"
    ]
)

result = problem.solve_interactive()

print("Punto óptimo:", result["optimal_point"])
print("Valor óptimo:", result["optimal_value"])

if result["interactive_plot"]:
    with open("complex_plot.html", "w", encoding="utf-8") as f:
        f.write(result["interactive_plot"])
    print("✅ Gráfico complejo guardado como 'complex_plot.html'")
    
    # Abrir en navegador
    import webbrowser
    webbrowser.open("complex_plot.html")