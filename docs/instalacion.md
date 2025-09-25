# Guia de instalación

## Requisitos del Sistema

- Python 3.11+
- pip (gestor de paquetes de Python)
- Git

## Instalación Local

### 1. Clonar el repositorio

### 2. Configurar el backend

cd backend
pip install -r requirements-prod.txt
python app.py

### 3. Configurar el frontend

cd frontend  
python -m http.server 8000

El frontend estará en : http://localhost:8000

## Configuración de Desarrollo

### Variables de Entorno

Crear un archivo .env en la carpeta backend

FLASK_ENV=development
PYTHONPATH=.


### Estructura de desarrollo

backend/
├── app.py                 # Aplicación principal
├── routes/
│   └── graphic_routes.py  # Endpoints API
└── utils/
    ├── graphic_method.py  # Lógica del método gráfico
    └── plotly_graphics.py # Generación de gráficos
	
## Solución de problemas

### Error: Módulo no encontrado

pip install flask flask-cors numpy matplotlib plotly scipy

### Error: Puerto en uso

**Cambiar puerto del backend**
python app.py --port 5001

**Cambiar puerto del frontend**  
python -m http.server 8001


