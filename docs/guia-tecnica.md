# Guía Técnica

## Arquitectura del sistema

### Frontend
- **HTML5/CSS3/JavaScript** vanilla
- **Plotly.js** para gráficos interactivos
- **Font Awesome** para iconos
- **Diseño responsive** con CSS Grid/Flexbox

### Backend
- **Flask** como framework web
- **Flask-CORS** para políticas de origen cruzado
- **NumPy/Matplotlib** para cálculos y gráficos estáticos
- **Plotly** para gráficos interactivos del lado del servidor

## Algoritmo del método gráfico

### 1. Parseo de restricciones

### 2. Cálculo de intersecciones

### 3. Determinacion de la region factible


## API Endpoints

### POST /api/graphic/solve/interactive
{
  "objective": "maximize 3x + 2y",
  "constraints": ["2x + y <= 100", "x + y <= 80"],
  "optimization_type": "maximize"
}

### POST /api/graphic/solve/static
{
  "objective": "minimize 4x + 3y", 
  "constraints": ["x + 2y >= 40", "3x + y >= 45"],
  "optimization_type": "minimize"
}

## Despliegue

### Backend (Render.com)
- Runtime: Python 3.11
- WSGI: Gunicorn
- Health check: /api/graphic/health

### Frontend (GitHub Pages)
- Build: GitHub Actions
- Source: Carpeta frontend/
- URL: https://matiusprog.github.io/investigacion-operativa-web/

