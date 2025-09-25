# Proyecto Métodos - Investigación Operativa
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-orange)

Web para resolver problemas de investigación operativa usando el método gráfico (de momento). El dia de hoy comenzamos con el trabaajo arduo

## Equipo
- [Luis Mateo Hurtado Castro]
- [Karen Paola Ortega Mancilla]
- [Marcos David Andrade Nove]

## Caracteristicas
- **Interfaz intuitiva** para ingresar funciones objetivo y restricciones
- **Gráficos interactivos** con Plotly para visualización en tiempo real
- **Gráficos estáticos** para exportación y documentación
- **Soporte para maximización y minimización**
- **Responsive design** que funciona en desktop y móvil
- **API RESTful** para integraciones futuras

## Demo en Vivo
- **Frontend:** [https://matiusprog.github.io/investigacion-operativa-web/](https://matiusprog.github.io/investigacion-operativa-web/)
- **Backend API:** [https://programacion-lineal-backend.onrender.com](https://programacion-lineal-backend.onrender.com)

## Estructura del Proyecto (resumida)
investigacion-operativa-web/
├── backend/ # API Flask
│ 	├── app.py # Aplicación principal
│ 	├── wsgi.py # Configuración producción
│ 	├── requirements-prod.txt
│ 	└── routes/ # Endpoints de la API
├── frontend/ # Interfaz web
│ 	├── index.html # Página principal
│ 	├── styles.css # Estilos
│ 	└── script.js # Lógica del cliente
└── docs/ # Documentación
	├── manual-usuario.md
	├── guia-tecnica.md
	└── api-reference.md
	
## Instalación Local
### Backend
```bash
cd backend
pip install -r requirements-prod.txt
python app.p ```
### Frontend
```cd frontend
python -m http.server 8000```

## Licencia

Este proyecto es para fines académicos como parte del curso de Investigación Operativa I

	*Universidad Gabriel René Moreno - 1-2025*

