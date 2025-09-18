from flask import Flask
from flask_cors import CORS
from routes.graphic_routes import graphic_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(graphic_bp, url_prefix='/api/graphic')
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Servidor Flask iniciado en http://localhost:5000")
    app.run(debug=True, port=5000)