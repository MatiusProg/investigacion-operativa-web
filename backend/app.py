# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configuración CORS mejorada
    def get_allowed_origins():
        origins = [
            "http://localhost:8000",
            "http://127.0.0.1:8000", 
            "http://localhost:3000",
            "https://matiusprog.github.io",
            "https://matiusprog.github.io/investigacion-operativa-web"
        ]
        
        # Agregar origen dinámico para desarrollo
        if os.environ.get('FLASK_ENV') != 'production':
            origins.append("*")  # Permitir todos en desarrollo
        
        return origins
    
    CORS(app, resources={
        r"/api/*": {
            "origins": get_allowed_origins(),
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Configuración adicional para producción
    if os.environ.get('FLASK_ENV') == 'production':
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
    
    # Importar y registrar rutas
    try:
        from routes.graphic_routes import graphic_bp
        app.register_blueprint(graphic_bp, url_prefix='/api/graphic')
        print("✅ Rutas de la API registradas correctamente")
    except ImportError as e:
        print(f"❌ Error importando rutas: {e}")
        @app.route('/api/graphic/health')
        def health_check():
            return {"status": "OK", "message": "Servidor funcionando"}
    
    return app

# Crear aplicación
app = create_app()

if __name__ == '__main__':
    print("🚀 Iniciando servidor...")
    app.run(debug=os.environ.get('FLASK_ENV') != 'production', host='0.0.0.0', port=5000)