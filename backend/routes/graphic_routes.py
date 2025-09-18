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
@graphic_bp.route('/solve/interactive', methods=['POST'])
def solve_interactive():
    try:
        data = request.get_json()
        
        if not data or 'objective' not in data or 'constraints' not in data:
            return jsonify({"error": "Datos incompletos"}), 400
        
        from utils.plotly_graphic import InteractiveLinearProgramming
        problem = InteractiveLinearProgramming(data['objective'], data['constraints'])
        
        result = problem.solve_interactive()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500