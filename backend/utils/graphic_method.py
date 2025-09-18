# -*- coding: utf-8 -*-
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

    def solve(self):
        all_points = self.find_all_intersections()
        feasible_points = []
        
        for point in all_points:
            feasible = all(self.is_feasible(point, c) for c in self.constraints)
            if feasible and point[0] >= 0 and point[1] >= 0:
                feasible_points.append(point)
        
        if not feasible_points:
            return {"error": "No existe solucion factible"}
        
        if "maximize" in self.objective:
            obj_type = "max"
            expr = self.objective.replace("maximize", "").strip()
        else:
            obj_type = "min"
            expr = self.objective.replace("minimize", "").strip()
        
        obj_x, obj_y = 0.0, 0.0
        
        if 'x' in expr:
            x_index = expr.find('x')
            if x_index > 0:
                num_str = expr[:x_index].strip()
                obj_x = float(num_str) if num_str not in ['+', '-'] else 1.0
            else:
                obj_x = 1.0
        
        if 'y' in expr:
            y_index = expr.find('y')
            if y_index > 0:
                num_str = expr[:y_index].strip()
                obj_y = float(num_str) if num_str not in ['+', '-'] else 1.0
            else:
                obj_y = 1.0
        
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