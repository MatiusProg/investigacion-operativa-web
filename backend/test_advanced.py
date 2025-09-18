# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.graphic_method import LinearProgrammingProblem

# Probar con diferentes problemas
test_cases = [
    {
        "name": "Problema 1 - Maximización",
        "objective": "maximize 3x + 2y",
        "constraints": ["2x + y <= 100", "x + y <= 80", "x >= 0", "y >= 0"]
    },
    {
        "name": "Problema 2 - Minimización", 
        "objective": "minimize 60x + 24y",
        "constraints": [
                        "x + y >= 65", 
                        "x>= 23", 
                        "y>=20",
                        "120x+200y<=12600", 
                        "x >= 0", 
                        "y >= 0"
                        ]
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'='*50}")
    print(f"🧪 {test_case['name']}")
    print(f"{'='*50}")
    
    problem = LinearProgrammingProblem(
        test_case["objective"],
        test_case["constraints"]
    )
    
    result = problem.solve_with_plot()
    
    print("Punto óptimo:", result["optimal_point"])
    print("Valor óptimo:", result["optimal_value"])
    print("Vértices factibles:", len(result["feasible_vertices"]))
    
    # Verificar solución
    verification = problem.verify_solution(
        result["feasible_vertices"], 
        result["optimal_point"]
    )
    print("Verificación:", verification)
    
    # Guardar gráfico
    if "plot" in result and result["plot"]:
        import base64
        with open(f"test_plot_{i}.png", "wb") as f:
            f.write(base64.b64decode(result["plot"]))
        print(f"Gráfico guardado como test_plot_{i}.png")

print(f"\n{'='*50}")
print("✅ Todas las pruebas completadas")
print(f"{'='*50}")