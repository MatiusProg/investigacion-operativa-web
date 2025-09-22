# -*- coding: utf-8 -*-
# type:ignore
from flask import Blueprint, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.graphic_method import LinearProgrammingProblem

graphic_bp = Blueprint('graphic', __name__)

@graphic_bp.route('/solve/interactive', methods=['POST'])
def solve_interactive():
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({"error": "No se proporcionaron datos JSON"}), 400
        
        if 'objective' not in data or not data['objective']:
            return jsonify({"error": "Falta la función objetivo"}), 400
            
        if 'constraints' not in data or not data['constraints'] or len(data['constraints']) == 0:
            return jsonify({"error": "Faltan restricciones"}), 400
        
        if 'optimization_type' not in data:
            return jsonify({"error": "Falta el tipo de optimización (maximize/minimize)"}), 400
        
        if len(data['constraints']) < 2:
            return jsonify({"error": "Se necesitan al menos 2 restricciones"}), 400
        
        # Importar y resolver
        from utils.plotly_graphics import InteractiveLinearProgramming
        problem = InteractiveLinearProgramming(data['objective'], data['constraints'])
        
        # Pasar el tipo de optimización al solve
        result = problem.solve_interactive(optimization_type=data['optimization_type'])
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error en /solve/interactive: {str(e)}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@graphic_bp.route('/solve/static', methods=['POST'])
def solve_static():
    try:
        data = request.get_json()
        print(f"📦 Datos recibidos en /static: {data}")  # ← LOG PARA DEBUG
        
        # Validaciones
        if not data:
            return jsonify({"error": "No se proporcionaron datos JSON"}), 400
        
        if 'objective' not in data or not data['objective']:
            return jsonify({"error": "Falta la función objetivo"}), 400
            
        if 'constraints' not in data or not data['constraints'] or len(data['constraints']) == 0:
            return jsonify({"error": "Faltan restricciones"}), 400
        
        if 'optimization_type' not in data:
            return jsonify({"error": "Falta el tipo de optimización"}), 400
        
        if len(data['constraints']) < 2:
            return jsonify({"error": "Se necesitan al menos 2 restricciones"}), 400
        
        # Resolver
        problem = LinearProgrammingProblem(data['objective'], data['constraints'])
        result = problem.solve_with_plot(optimization_type=data['optimization_type'])
        
        print(f"✅ Resultado estático: {result.get('plot') is not None}")  # ← LOG
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error en /solve/static: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@graphic_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud de la API"""
    return jsonify({
        "status": "OK", 
        "message": "Graphic method API is running",
        "version": "1.0",
        "endpoints": {
            "interactive": "/api/graphic/solve/interactive",
            "static": "/api/graphic/solve/static"
        }
    })

@graphic_bp.route('/example', methods=['GET'])
def get_example():
    """Endpoint que devuelve un problema de ejemplo"""
    example = {
        "objective": "maximize 3x + 2y",
        "constraints": [
            "2x + y <= 100",
            "x + y <= 80", 
            "x >= 0",
            "y >= 0"
        ],
        "description": "Problema ejemplo de maximización",
        "expected_solution": {
            "optimal_point": [20.0, 60.0],
            "optimal_value": 180.0
        }
    }
    return jsonify(example)