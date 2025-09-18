# -*- coding: utf-8 -*-
print("Probando estructura de paquetes...")

import os
import sys

# Verificar que los __init__.py existen
utils_init = os.path.exists('utils/__init__.py')
routes_init = os.path.exists('routes/__init__.py')

print("utils/__init__.py existe: " + str(utils_init))
print("routes/__init__.py existe: " + str(routes_init))

# Probar import
try:
    from utils.graphic_method import LinearProgrammingProblem
    print("Import directo exitoso")
except ImportError as e:
    print("Import directo fallo: " + str(e))
    
print("Prueba de estructura completada")