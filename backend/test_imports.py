# -*- coding: utf-8 -*-
print("Probando imports individuales...")

try:
    from flask import Flask
    print("✅ Flask importado")
except ImportError as e:
    print("❌ Error Flask:", e)

try:
    from flask_cors import CORS
    print("✅ CORS importado")
except ImportError as e:
    print("❌ Error CORS:", e)

try:
    from routes.graphic_routes import graphic_bp
    print("✅ graphic_bp importado")
except ImportError as e:
    print("❌ Error graphic_bp:", e)

print("Test completado")