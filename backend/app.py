# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from routes.graphic_routes import graphic_bp

def create_app():
    app = Flask(__name__)
    
    # Configuración CORS más específica
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "*"],
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    app.register_blueprint(graphic_bp, url_prefix='/api/graphic')
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Servidor Flask iniciado en http://localhost:5000")
    print("✅ CORS configurado para frontend en puerto 3000")
    print("📋 Endpoints disponibles:")
    print("   - POST /api/graphic/solve")
    print("   - GET  /api/graphic/health")
    print("   - POST /api/graphic/solve/interactive")
    app.run(debug=True, port=5000)