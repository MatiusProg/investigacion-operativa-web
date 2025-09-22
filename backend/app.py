# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configuración CORS para producción/desarrollo
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    if is_production:
        # En producción: dominios específicos
        frontend_urls = [
            "https://matiusprog.github.io",
            "https://matiusprog.github.io/investigacion-operativa-web",
            "http://localhost:3000"  # Para desarrollo local
        ]
    else:
        # En desarrollo: permitir todos los orígenes
        frontend_urls = "*"
    
    CORS(app, resources={
        r"/api/*": {
            "origins": frontend_urls,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Configuración adicional para producción
    if is_production:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
    
    # Importar y registrar rutas
    try:
        from routes.graphic_routes import graphic_bp
        app.register_blueprint(graphic_bp, url_prefix='/api/graphic')
        print("✅ Rutas de la API registradas correctamente")
    except ImportError as e:
        print(f"❌ Error importando rutas: {e}")
        # Crear ruta básica de salud para verificar que el servidor funciona
        @app.route('/api/graphic/health')
        def health_check():
            return {"status": "OK", "message": "Servidor funcionando"}
    
    return app

# Crear aplicación
app = create_app()

# Solo para ejecución local directa
if __name__ == '__main__':
    print("🚀 Iniciando servidor...")
    print("📊 Endpoints disponibles:")
    print("   • POST /api/graphic/solve/interactive")
    print("   • POST /api/graphic/solve/static")
    print("   • GET  /api/graphic/health")
    print("   • GET  /api/graphic/example")
    
    # Determinar si es producción
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)