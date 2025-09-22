// Configuración de API URL para producción/desarrollo
const getApiUrl = () => {
    const hostname = window.location.hostname;
    
    // Desarrollo local
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:5000/api/graphic';
    }
    
    // Producción - GitHub Pages
    return 'https://programacion-lineal-backend.onrender.com/api/graphic';
};

const API_URL = getApiUrl();
console.log('🌐 URL de API configurada:', API_URL);

// Estado de la aplicación
let currentSolution = null;
let currentTab = 'interactive';
let optimizationType = 'maximize';

// Función para cambiar tipo de optimización
function cambiarTipoOptimizacion(tipo) {
    optimizationType = tipo;
    
    document.querySelectorAll('.opt-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelector(`.opt-btn[data-type="${tipo}"]`).classList.add('active');
    console.log('Tipo de optimización:', optimizationType);
}

// Función para obtener restricciones
function obtenerRestricciones() {
    return Array.from(document.querySelectorAll('#restricciones input'))
        .map(input => input.value.trim())
        .filter(r => r !== '');
}

// Función para eliminar restricción
function eliminarRestriccion(boton) {
    const restrictionItem = boton.closest('.restriction-item');
    if (restrictionItem) {
        restrictionItem.remove();
    }
    
    const restricciones = document.querySelectorAll('#restricciones .restriction-item');
    if (restricciones.length === 0) {
        añadirRestriccion();
    }
}

// Función para añadir restricción
function añadirRestriccion() {
    const restriccionesDiv = document.getElementById('restricciones');
    const newItem = document.createElement('div');
    newItem.className = 'restriction-item';
    newItem.innerHTML = `
        <input type="text" placeholder="Ej: 2x + y <= 100">
        <button class="btn-remove-restriction" onclick="eliminarRestriccion(this)">
            <i class="fas fa-times"></i>
        </button>
    `;
    restriccionesDiv.appendChild(newItem);
}

// Función principal para resolver
async function resolverProblema() {
    const funcionObjetivo = document.getElementById('funcionObjetivo').value;
    const restricciones = obtenerRestricciones();

    if (!funcionObjetivo) {
        alert('Por favor, ingrese la función objetivo');
        return;
    }

    if (restricciones.length < 2) {
        alert('Se necesitan al menos 2 restricciones');
        return;
    }

    try {
        document.getElementById('solucion').innerHTML = `
            <div class="loading-container">
                <h3>Solución Óptima</h3>
                <div class="loading-spinner"></div>
                <p>Calculando solución...</p>
            </div>
        `;

        const response = await fetch(`${API_URL}/solve/interactive`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                objective: funcionObjetivo, 
                constraints: restricciones,
                optimization_type: optimizationType
            })
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log('📊 Datos recibidos:', data);

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        currentSolution = data;
        mostrarResultados(data, 'interactive');
        
    } catch (error) {
        console.error('❌ Error en resolverProblema:', error);
        alert('Error de conexión: ' + error.message);
    }
}

// Función para mostrar resultados
function mostrarResultados(data, tab) {
    currentTab = tab;
    
    let solucionHTML = `
        <div class="results-header">
            <h3>Solución Óptima</h3>
            <div class="tab-buttons">
                <button class="tab-btn ${tab === 'interactive' ? 'active' : ''}" onclick="cambiarPestaña('interactive')">
                    📊 Interactivo
                </button>
                <button class="tab-btn ${tab === 'static' ? 'active' : ''}" onclick="cambiarPestaña('static')">
                    📷 Exportar
                </button>
            </div>
        </div>
        <div class="numeric-results">
            <p><strong>Punto óptimo:</strong> (${data.optimal_point[0].toFixed(2)}, ${data.optimal_point[1].toFixed(2)})</p>
            <p><strong>Valor óptimo:</strong> ${data.optimal_value.toFixed(2)}</p>
            <p><strong>Vértices factibles:</strong> ${data.feasible_vertices.length} puntos</p>
        </div>
    `;

    let graficoHTML = '';
    
    if (tab === 'interactive' && data.interactive_plot) {
        graficoHTML = `
            <div class="plot-container">
                <h4>Gráfico Interactivo</h4>
                <div id="plotly-container">${data.interactive_plot}</div>
            </div>
        `;
    } else if (tab === 'static' && data.plot) {
        graficoHTML = `
            <div class="plot-container">
                <h4>Gráfico para Exportar</h4>
                <img src="data:image/png;base64,${data.plot}" alt="Gráfico" class="export-image">
                <button class="btn-export" onclick="exportarPNG()">💾 Descargar PNG</button>
            </div>
        `;
    } else {
        graficoHTML = `<p class="no-chart-message">Selecciona un modo de visualización</p>`;
    }

    document.getElementById('solucion').innerHTML = solucionHTML;
    document.getElementById('grafico-interactivo').innerHTML = graficoHTML;

    if (tab === 'interactive' && data.interactive_plot) {
        setTimeout(initializePlotlyInteractive, 300);
    }
}

// Función para inicializar Plotly
function initializePlotlyInteractive() {
    const container = document.getElementById('plotly-container');
    if (!container) return;
    
    console.log('✅ Inicializando gráfico interactivo...');
    
    // Esperar a que Plotly esté disponible
    const checkPlotlyLoaded = setInterval(() => {
        if (typeof Plotly !== 'undefined') {
            clearInterval(checkPlotlyLoaded);
            console.log('🎯 Plotly cargado, ejecutando scripts...');
            ejecutarScriptsPlotly();
        }
    }, 100);
}

// Función para ejecutar scripts de Plotly
function ejecutarScriptsPlotly() {
    const scripts = document.querySelectorAll('#plotly-container script');
    console.log(`📜 Encontrados ${scripts.length} scripts`);
    
    scripts.forEach((script, index) => {
        try {
            const newScript = document.createElement('script');
            if (script.src) {
                newScript.src = script.src;
                newScript.async = true;
            } else {
                newScript.textContent = script.textContent;
            }
            document.head.appendChild(newScript);
            console.log(`✅ Script ${index + 1} ejecutado`);
        } catch (error) {
            console.log(`❌ Error en script ${index + 1}:`, error);
        }
    });
}

// Función para cambiar pestañas
async function cambiarPestaña(tab) {
    if (!currentSolution) return;
    
    if (tab === 'interactive' && currentSolution.interactive_plot) {
        mostrarResultados(currentSolution, tab);
        return;
    }
    
    document.getElementById('grafico-interactivo').innerHTML = `
        <div class="plotly-loading">
            <div class="plotly-spinner"></div>
            <p>Cargando ${tab === 'interactive' ? 'interactivo' : 'exportar'}...</p>
        </div>
    `;
    
    if (tab === 'static') {
        try {
            if (!currentSolution.plot) {
                const response = await fetch(`${API_URL}/solve/static`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        objective: document.getElementById('funcionObjetivo').value, 
                        constraints: obtenerRestricciones(),
                        optimization_type: optimizationType
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                
                const staticData = await response.json();
                if (staticData.error) throw new Error(staticData.error);
                
                currentSolution.plot = staticData.plot;
            }
        } catch (error) {
            document.getElementById('grafico-interactivo').innerHTML = `
                <div class="error-container">
                    <p>Error: ${error.message}</p>
                    <button class="btn-retry" onclick="cambiarPestaña('static')">Reintentar</button>
                </div>
            `;
            return;
        }
    }
    
    mostrarResultados(currentSolution, tab);
}

// Función para exportar PNG
function exportarPNG() {
    if (!currentSolution?.plot) {
        alert('No hay gráfico para exportar');
        return;
    }

    const link = document.createElement('a');
    link.href = 'data:image/png;base64,' + currentSolution.plot;
    link.download = 'solucion_metodo_grafico.png';
    link.click();
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Botones de optimización
    document.querySelectorAll('.opt-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            cambiarTipoOptimizacion(this.dataset.type);
        });
    });
    
    // Botón resolver
    document.querySelector('.btn-resolver').addEventListener('click', resolverProblema);
    
    console.log('✅ Aplicación inicializada. API URL:', API_URL);
});

// Remover console.log en producción (solo mantener para desarrollo)
if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    console.log = function() {}; // Silenciar console.log en producción
}