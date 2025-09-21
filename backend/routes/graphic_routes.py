# -*- coding: utf-8 -*-
# type:ignore
from flask import Blueprint, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.graphic_method import LinearProgrammingProblem

graphic_bp = Blueprint('graphic', __name__)

@graphic_bp.route('/solve', methods=['POST'])
def solve_problem():
    try:
        data = request.get_json()
        
        if not data or 'objective' not in data or 'constraints' not in data:
            return jsonify({"error": "Datos incompletos"}), 400
        
        problem = LinearProgrammingProblem(
            data['objective'],
            data['constraints']
        )
        
        # Usar solve_with_plot que incluye gráfico
        result = problem.solve_with_plot()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@graphic_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "message": "Graphic method API is running"})
@graphic_bp.route('/solve', methods=['POST'])
def solve_problem():
    try:
        data = request.get_json()
        
        # Validaciones más exhaustivas
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        if 'objective' not in data or not data['objective']:
            return jsonify({"error": "Falta la función objetivo"}), 400
            
        if 'constraints' not in data or not data['constraints'] or len(data['constraints']) == 0:
            return jsonify({"error": "Faltan restricciones"}), 400
        
        # Validar que hay al menos 2 restricciones para un problema bidimensional
        if len(data['constraints']) < 2:
            return jsonify({"error": "Se necesitan al menos 2 restricciones"}), 400
        
        problem = LinearProgrammingProblem(
            data['objective'],
            data['constraints']
        )
        
        result = problem.solve_with_plot()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500