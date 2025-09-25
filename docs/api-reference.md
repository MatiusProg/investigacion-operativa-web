# Referencia de la API

## Base URL
https://programacion-lineal-backend.onrender.com/api/graphic

## Endpoints

### Health Check
**GET** /health

{
  "status": "OK",
  "message": "Graphic method API is running",
  "version": "1.0",
  "endpoints": {
    "interactive": "/api/graphic/solve/interactive",
    "static": "/api/graphic/solve/static"
  }
}

### Resolver Problema Interactivo
**POST** /solve/interactive

*Body:*
{
  "objective": "maximize 3x + 2y",
  "constraints": [
    "2x + y <= 100",
    "x + y <= 80", 
    "x >= 0",
    "y >= 0"
  ],
  "optimization_type": "maximize"
}

*Response:*
{
  "optimal_point": [20.0, 60.0],
  "optimal_value": 180.0,
  "feasible_vertices": [[0,0], [50,0], [20,60], [0,80]],
  "interactive_plot": "<div>...HTML de Plotly...</div>"
}

### Resolver Problema Estático

**POST** /solve/static

*Response:*
{
  "optimal_point": [20.0, 60.0], 
  "optimal_value": 180.0,
  "feasible_vertices": [[0,0], [50,0], [20,60], [0,80]],
  "plot": "base64_encoded_image"
}

### Ejemplo de Uso con JavaScript

const solveProblem = async () => {
  const response = await fetch('/api/graphic/solve/interactive', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      objective: 'maximize 3x + 2y',
      constraints: ['2x + y <= 100', 'x + y <= 80'],
      optimization_type: 'maximize'
    })
  });
  
  const result = await response.json();
  document.getElementById('plot-container').innerHTML = result.interactive_plot;
};

### Códigos de Error
- 400: Datos de entrada inválidos
- 500: Error interno del servidor