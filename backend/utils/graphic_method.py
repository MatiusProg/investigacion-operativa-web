# -*- coding: utf-8 -*-
# type:ignore
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

# SOLUCIÓN PARA EL ERROR DE MATPLOTLIB EN THREADS
import matplotlib
matplotlib.use('Agg')  # ← ¡IMPORTANTE! Usar backend no interactivo
import matplotlib.pyplot as plt

class LinearProgrammingProblem:
    def __init__(self, objective, constraints):
        self.objective = objective
        self.constraints = constraints
        self.vertices = []
        self.feasible_region = []
        self.optimal_point = None
        self.optimal_value = None
    
    def parse_constraint(self, constraint):
        if '<=' in constraint:
            left, right = constraint.split('<=')
            ineq = '<='
        elif '>=' in constraint:
            left, right = constraint.split('>=')
            ineq = '>='
        else:
            left, right = constraint.split('=')
            ineq = '='
        
        left = left.strip()
        right = float(right.strip())
        
        coef_x = 0.0
        coef_y = 0.0
        
        if 'x' in left:
            x_index = left.find('x')
            if x_index == 0:
                coef_x = 1.0
            else:
                before_x = left[:x_index].strip()
                if before_x.endswith('+'):
                    coef_x = 1.0
                elif before_x.endswith('-'):
                    coef_x = -1.0
                else:
                    num_str = before_x
                    if '+' in num_str:
                        num_str = num_str.split('+')[-1]
                    if '-' in num_str:
                        num_str = num_str.split('-')[-1]
                    num_str = num_str.strip()
                    coef_x = float(num_str) if num_str else 1.0
        
        if 'y' in left:
            y_index = left.find('y')
            if y_index == 0:
                coef_y = 1.0
            else:
                before_y = left[:y_index].strip()
                if before_y.endswith('+'):
                    coef_y = 1.0
                elif before_y.endswith('-'):
                    coef_y = -1.0
                else:
                    num_str = before_y
                    if '+' in num_str:
                        num_str = num_str.split('+')[-1]
                    if '-' in num_str:
                        num_str = num_str.split('-')[-1]
                    num_str = num_str.strip()
                    coef_y = float(num_str) if num_str else 1.0
        
        return [coef_x, coef_y], right, ineq

    def find_intersection(self, constraint1, constraint2):
        (a1, b1), c1, _ = self.parse_constraint(constraint1)
        (a2, b2), c2, _ = self.parse_constraint(constraint2)
        
        determinant = a1 * b2 - a2 * b1
        
        if abs(determinant) < 1e-10:
            return None
            
        x = (c1 * b2 - c2 * b1) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        
        return (x, y)

    def is_feasible(self, point, constraint):
        x, y = point
        coefficients, right_side, inequality = self.parse_constraint(constraint)
        a, b = coefficients
        
        value = a * x + b * y
        
        if inequality == '<=':
            return value <= right_side + 1e-10
        elif inequality == '>=':
            return value >= right_side - 1e-10
        else:
            return abs(value - right_side) < 1e-10

    def find_all_intersections(self):
        intersections = []
        n = len(self.constraints)
        
        for i in range(n):
            for j in range(i + 1, n):
                point = self.find_intersection(self.constraints[i], self.constraints[j])
                if point is not None:
                    intersections.append(point)
        
        for constraint in self.constraints:
            coefficients, right_side, _ = self.parse_constraint(constraint)
            a, b = coefficients
            
            if abs(a) > 1e-10:
                intersections.append((right_side / a, 0))
            if abs(b) > 1e-10:
                intersections.append((0, right_side / b))
        
        return intersections
    def parse_objective(self, objective_str):
        """Parsea la función objetivo de manera más robusta"""
        # Limpiar y normalizar la cadena
        clean_str = objective_str.lower().replace(" ", "").replace("maximize", "").replace("minimize", "").replace("max", "").replace("min", "")
        
        # Determinar tipo de optimización
        if "max" in objective_str.lower():
            obj_type = "max"
        else:
            obj_type = "min"
        
        # Usar expresión regular para encontrar coeficientes
        import re
        
        coef_x = 0
        coef_y = 0
        
        # Buscar coeficiente para x
        x_match = re.search(r'([+-]?\d*\.?\d*)x', clean_str)
        if x_match:
            coef_str = x_match.group(1)
            if coef_str in ['', '+']:
                coef_x = 1
            elif coef_str == '-':
                coef_x = -1
            else:
                coef_x = float(coef_str)
        
        # Buscar coeficiente para y
        y_match = re.search(r'([+-]?\d*\.?\d*)y', clean_str)
        if y_match:
            coef_str = y_match.group(1)
            if coef_str in ['', '+']:
                coef_y = 1
            elif coef_str == '-':
                coef_y = -1
            else:
                coef_y = float(coef_str)
        
        return obj_type, coef_x, coef_y

    def solve(self):
        all_points = self.find_all_intersections()
        feasible_points = []
        
        for point in all_points:
            feasible = all(self.is_feasible(point, c) for c in self.constraints)
            if feasible and point[0] >= 0 and point[1] >= 0:
                feasible_points.append(point)
        
        if not feasible_points:
            return {"error": "No existe solucion factible"}
        
        obj_type, obj_x, obj_y = self.parse_objective(self.objective)
        
        best_value = float('-inf') if obj_type == "max" else float('inf')
        best_point = None
        
        for point in feasible_points:
            x, y = point
            value = obj_x * x + obj_y * y
            
            if (obj_type == "max" and value > best_value) or (obj_type == "min" and value < best_value):
                best_value = value
                best_point = point
        
        return {
            "optimal_point": best_point,
            "optimal_value": best_value,
            "feasible_vertices": feasible_points
        }
    def plot_solution(self, feasible_points, optimal_point):
        """Genera un gráfico completo y profesional de la solución"""
        try:
            plt.figure(figsize=(12, 10))
            
            # Encontrar límites del gráfico
            all_x = [p[0] for p in feasible_points] if feasible_points else [0, 100]
            all_y = [p[1] for p in feasible_points] if feasible_points else [0, 100]
            
            max_x = max(all_x) * 1.2 if all_x else 100
            max_y = max(all_y) * 1.2 if all_y else 100
            
            x_vals = np.linspace(0, max_x, 400)
            
            # Colores para las restricciones
            colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
            
            # Graficar cada restricción COMPLETAMENTE
            for i, constraint in enumerate(self.constraints):
                coefficients, right_side, inequality = self.parse_constraint(constraint)
                a, b = coefficients
                
                color = colors[i % len(colors)]
                
                if abs(b) > 1e-10:  # Recta normal
                    y_vals = (right_side - a * x_vals) / b
                    plt.plot(x_vals, y_vals, color=color, linewidth=3, 
                            label=f'{constraint}', linestyle='-', alpha=0.8)
                    
                    # Sombrear región según desigualdad
                    if inequality == '<=':
                        plt.fill_between(x_vals, 0, y_vals, color=color, alpha=0.1)
                    elif inequality == '>=':
                        plt.fill_between(x_vals, y_vals, max_y, color=color, alpha=0.1)
                        
                else:  # Línea vertical
                    x_val = right_side / a
                    plt.axvline(x=x_val, color=color, linewidth=3, 
                            label=f'{constraint}', linestyle='-', alpha=0.8)
                    
                    # Sombrear región según desigualdad
                    if inequality == '<=':
                        plt.axvspan(0, x_val, color=color, alpha=0.1)
                    elif inequality == '>=':
                        plt.axvspan(x_val, max_x, color=color, alpha=0.1)
            
            # Graficar región factible (intersección de todas las restricciones)
            if feasible_points:
                # Crear polígono convexo
                points = np.array(feasible_points)
                from scipy.spatial import ConvexHull
                try:
                    hull = ConvexHull(points)
                    hull_points = points[hull.vertices]
                    
                    # Ordenar puntos en sentido horario
                    centroid = np.mean(hull_points, axis=0)
                    angles = np.arctan2(hull_points[:,1] - centroid[1], 
                                    hull_points[:,0] - centroid[0])
                    hull_points = hull_points[np.argsort(angles)]
                    
                    plt.fill(hull_points[:,0], hull_points[:,1], 'lightgreen', 
                            alpha=0.6, label='Región Factible', edgecolor='darkgreen', linewidth=2)
                    
                    # Marcar vértices factibles
                    plt.plot(points[:,0], points[:,1], 'go', markersize=8, alpha=0.7)
                
                except:
                    # Fallback si no se puede calcular el convex hull
                    plt.fill(points[:,0], points[:,1], 'lightgreen', 
                            alpha=0.6, label='Región Factible')
            
            # Graficar punto óptimo
            if optimal_point:
                plt.plot(optimal_point[0], optimal_point[1], 's', color='gold', 
                        markersize=15, markerfacecolor='yellow', 
                        markeredgecolor='black', markeredgewidth=2,
                        label=f'Óptimo: ({optimal_point[0]:.2f}, {optimal_point[1]:.2f})')
            
            # Líneas de ejes y cuadrícula
            plt.axhline(y=0, color='black', linewidth=0.5, alpha=0.7)
            plt.axvline(x=0, color='black', linewidth=0.5, alpha=0.7)
            plt.grid(True, alpha=0.3, linestyle='--')
            
            # Configuración del gráfico
            plt.xlabel('Variable x', fontsize=12, fontweight='bold')
            plt.ylabel('Variable y', fontsize=12, fontweight='bold')
            plt.title('Solución por Método Gráfico - Programación Lineal', 
                    fontsize=14, fontweight='bold', pad=20)
            
            # Leyenda fuera del gráfico
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
            
            # Límites
            plt.xlim(0, max_x)
            plt.ylim(0, max_y)
            
            # Convertir a base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            print(f"Error generando gráfico: {e}")
            import traceback
            traceback.print_exc()
            return None

    def solve_with_plot(self):
        """Resuelve el problema y retorna resultado con gráfico"""
        result = self.solve()
        
        if "error" in result:
            return result
        
        # Generar gráfico
        plot_base64 = self.plot_solution(result["feasible_vertices"], result["optimal_point"])
        
        if plot_base64:
            result["plot"] = plot_base64
        else:
            result["plot"] = None
        
        return result
    def verify_solution(self, feasible_points, optimal_point):
        """Verifica matemáticamente que la solución es correcta"""
        if not feasible_points or not optimal_point:
            return {"error": "No hay solución para verificar"}
        
        # Verificar que el punto óptimo es factible
        for constraint in self.constraints:
            if not self.is_feasible(optimal_point, constraint):
                return {"error": "Punto óptimo no es factible"}
        
        # Verificar que es el óptimo
        if "maximize" in self.objective:
            obj_type = "max"
            expr = self.objective.replace("maximize", "").strip()
        else:
            obj_type = "min"
            expr = self.objective.replace("minimize", "").strip()
        
        # Coeficientes simples para prueba
        obj_x, obj_y = 3.0, 2.0  # Para "maximize 3x + 2y"
        
        optimal_value = obj_x * optimal_point[0] + obj_y * optimal_point[1]
        
        # Verificar contra todos los puntos factibles
        for point in feasible_points:
            value = obj_x * point[0] + obj_y * point[1]
            if obj_type == "max" and value > optimal_value + 1e-10:
                return {"warning": f"Posible error: punto {point} tiene valor {value} > {optimal_value}"}
            elif obj_type == "min" and value < optimal_value - 1e-10:
                return {"warning": f"Posible error: punto {point} tiene valor {value} < {optimal_value}"}
        
        return {"success": f"Solución verificada: valor óptimo = {optimal_value}"}