// Configuracion de API URL para produccion/desarrollo
const getApiUrl = () => {
    const hostname = window.location.hostname;
    
    // Desarrollo local
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:5000/api/graphic';
    }
    
    // Produccion - GitHub Pages
    return 'https://programacion-lineal-backend.onrender.com/api/graphic';
};

const API_URL = getApiUrl();
console.log('URL de API configurada:', API_URL);

// Estado de la aplicacion
let currentSolution = null;
let currentTab = 'interactive';
let optimizationType = 'maximize';

// Funcion para cambiar tipo de optimizacion
function cambiarTipoOptimizacion(tipo) {
    optimizationType = tipo;
    
    document.querySelectorAll('.opt-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelector(`.opt-btn[data-type="${tipo}"]`).classList.add('active');
    console.log('Tipo de optimizacion:', optimizationType);
}

// Funcion para obtener restricciones
function obtenerRestricciones() {
    return Array.from(document.querySelectorAll('#restricciones input'))
        .map(input => input.value.trim())
        .filter(r => r !== '');
}

// Funcion para eliminar restriccion
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

// Funcion para añadir restriccion
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

// Funcion principal para resolver
async function resolverProblema() {
    const funcionObjetivo = document.getElementById('funcionObjetivo').value;
    const restricciones = obtenerRestricciones();

    if (!funcionObjetivo) {
        alert('Por favor, ingrese la funcion objetivo');
        return;
    }

    if (restricciones.length < 2) {
        alert('Se necesitan al menos 2 restricciones');
        return;
    }

    try {
        document.getElementById('solucion').innerHTML = `
            <div class="loading-container">
                <h3>Solucion Optima</h3>
                <div class="loading-spinner"></div>
                <p>Calculando solucion...</p>
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
        console.log('Datos recibidos:', data);

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        currentSolution = data;
        mostrarResultados(data, 'interactive');
        
    } catch (error) {
        console.error('Error en resolverProblema:', error);
        alert('Error de conexion: ' + error.message);
    }
}

// Funcion para mostrar resultados
function mostrarResultados(data, tab) {
    currentTab = tab;
    
    let solucionHTML = `
        <div class="results-header">
            <h3>Solucion Optima</h3>
            <div class="tab-buttons">
                <button class="tab-btn ${tab === 'interactive' ? 'active' : ''}" onclick="cambiarPestana('interactive')">
                    Interactivo
                </button>
                <button class="tab-btn ${tab === 'static' ? 'active' : ''}" onclick="cambiarPestana('static')">
                    Exportar
                </button>
            </div>
        </div>
        <div class="numeric-results">
            <p><strong>Punto optimo:</strong> (${data.optimal_point[0].toFixed(2)}, ${data.optimal_point[1].toFixed(2)})</p>
            <p><strong>Valor optimo:</strong> ${data.optimal_value.toFixed(2)}</p>
            <p><strong>Vertices factibles:</strong> ${data.feasible_vertices.length} puntos</p>
        </div>
    `;

    let graficoHTML = '';
    
    if (tab === 'interactive' && data.interactive_plot) {
        graficoHTML = `
            <div class="plot-container">
                <h4>Grafico Interactivo</h4>
                <div id="plotly-container">${data.interactive_plot}</div>
            </div>
        `;
    } else if (tab === 'static' && data.plot) {
        graficoHTML = `
            <div class="plot-container">
                <h4>Grafico para Exportar</h4>
                <img src="data:image/png;base64,${data.plot}" alt="Grafico" class="export-image">
                <button class="btn-export" onclick="exportarPNG()">Descargar PNG</button>
            </div>
        `;
    } else {
        graficoHTML = `<p class="no-chart-message">Selecciona un modo de visualizacion</p>`;
    }

    document.getElementById('solucion').innerHTML = solucionHTML;
    document.getElementById('grafico-interactivo').innerHTML = graficoHTML;

    if (tab === 'interactive' && data.interactive_plot) {
        setTimeout(initializePlotlyInteractive, 300);
    }
}

// Funcion para inicializar Plotly
function initializePlotlyInteractive() {
    const container = document.getElementById('plotly-container');
    if (!container) return;
    
    console.log('Inicializando grafico interactivo...');
    
    // Esperar a que Plotly este disponible
    const checkPlotlyLoaded = setInterval(() => {
        if (typeof Plotly !== 'undefined') {
            clearInterval(checkPlotlyLoaded);
            console.log('Plotly cargado, ejecutando scripts...');
            ejecutarScriptsPlotly();
            
            // Verificar después de un tiempo si se renderizo
            setTimeout(() => {
                const plotlyDiv = container.querySelector('.plotly-graph-div');
                if (!plotlyDiv || plotlyDiv.children.length === 0) {
                    console.log('Grafico no renderizado, intentando recrear...');
                    recrearPlotlyDesdeDatos();
                } else {
                    console.log('Grafico interactivo mostrado correctamente');
                }
            }, 1000);
        }
    }, 100);
    
    // Timeout de seguridad
    setTimeout(() => {
        clearInterval(checkPlotlyLoaded);
        if (typeof Plotly === 'undefined') {
            console.log('Timeout: Cargando Plotly manualmente...');
            cargarPlotlyManualmente();
        }
    }, 5000);
}

// Funcion para ejecutar scripts de Plotly
function ejecutarScriptsPlotly() {
    const scripts = document.querySelectorAll('#plotly-container script');
    console.log(`Encontrados ${scripts.length} scripts`);
    
    // Verificar si Plotly esta cargado primero
    if (typeof Plotly === 'undefined') {
        console.log('Plotly no esta cargado, esperando...');
        setTimeout(ejecutarScriptsPlotly, 100);
        return;
    }
    
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
            console.log(`Script ${index + 1} ejecutado`);
        } catch (error) {
            console.log(`Error en script ${index + 1}:`, error);
        }
    });
}

// Funcion para cargar Plotly manualmente
function cargarPlotlyManualmente() {
    if (typeof Plotly === 'undefined') {
        console.log('Cargando Plotly desde CDN...');
        const script = document.createElement('script');
        script.src = 'https://cdn.plot.ly/plotly-3.1.0.min.js';
        script.onload = function() {
            console.log('Plotly cargado manualmente');
            ejecutarScriptsPlotly();
        };
        document.head.appendChild(script);
    } else {
        ejecutarScriptsPlotly();
    }
}

// Funcion para recrear Plotly desde los datos
function recrearPlotlyDesdeDatos() {
    const container = document.getElementById('plotly-container');
    if (!container) return;
    
    const script = container.querySelector('script');
    if (!script) return;
    
    try {
        // Extraer datos del script
        const scriptContent = script.textContent;
        const newPlotMatch = scriptContent.match(/Plotly\.newPlot\(['"]([^'"]+)['"],\s*(\[.*?\]),\s*(\{.*?\}),\s*(\{.*?\})\)/s);
        
        if (newPlotMatch && typeof Plotly !== 'undefined') {
            const [_, id, dataStr, layoutStr, configStr] = newPlotMatch;
            
            // Parsear datos
            const data = JSON.parse(dataStr);
            const layout = JSON.parse(layoutStr);
            const config = JSON.parse(configStr);
            
            // Limpiar contenedor y recrear
            container.innerHTML = `<div id="${id}"></div>`;
            Plotly.newPlot(id, data, layout, config);
            
            console.log('Grafico recreado manualmente desde datos');
        }
    } catch (error) {
        console.log('Error recreando grafico:', error);
    }
}

// Funcion para cambiar pestanas
async function cambiarPestana(tab) {
    if (!currentSolution) return;
    
    // Si vamos a interactivo y ya tenemos el grafico, solo mostrarlo
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
                    <button class="btn-retry" onclick="cambiarPestana('static')">Reintentar</button>
                </div>
            `;
            return;
        }
    }
    
    mostrarResultados(currentSolution, tab);
}

// Funcion para exportar PNG
function exportarPNG() {
    if (!currentSolution?.plot) {
        alert('No hay grafico para exportar');
        return;
    }

    const link = document.createElement('a');
    link.href = 'data:image/png;base64,' + currentSolution.plot;
    link.download = 'solucion_metodo_grafico.png';
    link.click();
}

// Inicializacion
document.addEventListener('DOMContentLoaded', function() {
    // Botones de optimizacion
    document.querySelectorAll('.opt-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            cambiarTipoOptimizacion(this.dataset.type);
        });
    });
    
    // Cerrar menu
    document.getElementById('closeMenu').addEventListener('click', function() {
        document.querySelector('.sidebar').classList.remove('active');
    });
    
    // Boton resolver
    document.querySelector('.btn-resolver').addEventListener('click', resolverProblema);
    
    // Añadir restriccion
    const addButton = document.getElementById('addRestriccion');
    if (addButton) {
        addButton.addEventListener('click', function(e) {
            e.preventDefault();
            añadirRestriccion();
        });
    }
    
    console.log('Aplicacion inicializada. API URL:', API_URL);
});

// Remover console.log en produccion (solo mantener para desarrollo)
if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    console.log = function() {}; // Silenciar console.log en produccion
}