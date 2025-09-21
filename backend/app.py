# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Configuración CORS más específica
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000", 
                       "http://localhost:5500", "http://127.0.0.1:5500", "*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Importar y registrar las rutas
    try:
        from routes.graphic_routes import graphic_bp
        app.register_blueprint(graphic_bp, url_prefix='/api/graphic')
        print("✅ Rutas de la API registradas correctamente")
    except ImportError as e:
        print(f"❌ Error importando rutas: {e}")
        # Crear rutas básicas si falla la importación
        @app.route('/api/graphic/health')
        def health_fallback():
            return {"status": "OK", "message": "API funcionando (modo fallback)"}
    
    return app

if __name__ == '__main__':
    # Crear y ejecutar la aplicación
    app = create_app()
    
    print("\n" + "="*50)
    print("🚀 Servidor Flask de Programación Lineal")
    print("="*50)
    print("📋 Endpoints disponibles:")
    print("   • GET  http://localhost:5000/api/graphic/health")
    print("   • GET  http://localhost:5000/api/graphic/example") 
    print("   • POST http://localhost:5000/api/graphic/solve/interactive")
    print("   • POST http://localhost:5000/api/graphic/solve/static")
    print("")
    print("🌐 Frontend debe conectarse desde:")
    print("   • http://localhost:3000 (Live Server)")
    print("   • http://localhost:5500 (VS Code)")
    print("   • o abrir directamente index.html")
    print("="*50)
    print("\nPresiona Ctrl+C para detener el servidor\n")
    
    # Ejecutar la aplicación
    app.run(debug=True, port=5000, host='0.0.0.0')