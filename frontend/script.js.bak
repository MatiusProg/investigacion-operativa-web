// Configuraci®Æn de API URL para producci®Æn/desarrollo
const getApiUrl = () => {
    const hostname = window.location.hostname;
    
    // Desarrollo local
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:5000/api/graphic';
    }
    
    // Producci®Æn - GitHub Pages
    return 'https://programacion-lineal-backend.onrender.com';
};

const API_URL = getApiUrl();
console.log('La URL de API configurada:', API_URL);

// Estado de la aplicaci®Æn
let currentSolution = null;
let currentTab = 'interactive';
let optimizationType = 'maximize';

// Funci®Æn para cambiar tipo de optimizaci√≥n
function cambiarTipoOptimizacion(tipo) {
    optimizationType = tipo;
    
    document.querySelectorAll('.opt-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelector(`.opt-btn[data-type="${tipo}"]`).classList.add('active');
    console.log('Tipo de optimizaci®Æn:', optimizationType);
}

// Funci®Æn para obtener restricciones
function obtenerRestricciones() {
    return Array.from(document.querySelectorAll('#restricciones input'))
        .map(input => input.value.trim())
        .filter(r => r !== '');
}

// Funci®Æn para eliminar restricci®Æn
function eliminarRestriccion(boton) {
    const restrictionItem = boton.closest('.restriction-item');
    if (restrictionItem) {
        restrictionItem.remove();
    }
    
    const restricciones = document.querySelectorAll('#restricciones .restriction-item');
    if (restricciones.length === 0) {
        a√±adirRestriccion();
    }
}

// Funci®Æn para a?adir restricci√≥n
function a√±adirRestriccion() {
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

// Funci®Æn principal para resolver
async function resolverProblema() {
    const funcionObjetivo = document.getElementById('funcionObjetivo').value;
    const restricciones = obtenerRestricciones();

    if (!funcionObjetivo) {
        alert('Por favor, ingrese la funci√≥n objetivo');
        return;
    }

    if (restricciones.length < 2) {
        alert('Se necesitan al menos 2 restricciones');
        return;
    }

    try {
        document.getElementById('solucion').innerHTML = `
            <div class="loading-container">
                <h3>Soluci®Æn ®Æptima</h3>
                <div class="loading-spinner"></div>
                <p>Calculando soluci®Æn...</p>
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
        console.log('üìä Datos recibidos:', data);

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        currentSolution = data;
        mostrarResultados(data, 'interactive');
        
    } catch (error) {
        console.error('‚ù?Error en resolverProblema:', error);
        alert('Error de conexi®Æn: ' + error.message);
    }
}

// Funci®Æn para mostrar resultados
function mostrarResultados(data, tab) {
    currentTab = tab;
    
    let solucionHTML = `
        <div class="results-header">
            <h3>Soluci®Æn ®Æptima</h3>
            <div class="tab-buttons">
                <button class="tab-btn ${tab === 'interactive' ? 'active' : ''}" onclick="cambiarPesta?a('interactive')">
                    üìä Interactivo
                </button>
                <button class="tab-btn ${tab === 'static' ? 'active' : ''}" onclick="cambiarPesta√±a('static')">
                    üì∑ Exportar
                </button>
            </div>
        </div>
        <div class="numeric-results">
            <p><strong>Punto ®Æptimo:</strong> (${data.optimal_point[0].toFixed(2)}, ${data.optimal_point[1].toFixed(2)})</p>
            <p><strong>Valor ®Æptimo:</strong> ${data.optimal_value.toFixed(2)}</p>
            <p><strong>V√©rtices factibles:</strong> ${data.feasible_vertices.length} puntos</p>
        </div>
    `;

    let graficoHTML = '';
    
    if (tab === 'interactive' && data.interactive_plot) {
        graficoHTML = `
            <div class="plot-container">
                <h4>Gr®¢fico Interactivo</h4>
                <div id="plotly-container">${data.interactive_plot}</div>
            </div>
        `;
    } else if (tab === 'static' && data.plot) {
        graficoHTML = `
            <div class="plot-container">
                <h4>Gr®¢fico para Exportar</h4>
                <img src="data:image/png;base64,${data.plot}" alt="Gr®¢fico" class="export-image">
                <button class="btn-export" onclick="exportarPNG()">üíæ Descargar PNG</button>
            </div>
        `;
    } else {
        graficoHTML = `<p class="no-chart-message">Selecciona un modo de visualizaci®Æn</p>`;
    }

    document.getElementById('solucion').innerHTML = solucionHTML;
    document.getElementById('grafico-interactivo').innerHTML = graficoHTML;

    if (tab === 'interactive' && data.interactive_plot) {
        setTimeout(initializePlotlyInteractive, 300);
    }
}

// Funci®Æn para inicializar Plotly
function initializePlotlyInteractive() {
    const container = document.getElementById('plotly-container');
    if (!container) return;
    
    console.log('‚ú?Inicializando gr®¢fico interactivo...');
    
    // Esperar a que Plotly est®¢ disponible
    const checkPlotlyLoaded = setInterval(() => {
        if (typeof Plotly !== 'undefined') {
            clearInterval(checkPlotlyLoaded);
            console.log('üéØ Plotly cargado, ejecutando scripts...');
            ejecutarScriptsPlotly();
            
            // Verificar despu®¶s de un tiempo si se renderiza
            setTimeout(() => {
                const plotlyDiv = container.querySelector('.plotly-graph-div');
                if (!plotlyDiv || plotlyDiv.children.length === 0) {
                    console.log('‚ö†Ô∏è  Gr®¢fico no renderizado, intentando recrear...');
                    recrearPlotlyDesdeDatos();
                } else {
                    console.log('‚ú?Gr®¢fico interactivo mostrado correctamente');
                }
            }, 1000);
        }
    }, 100);
    
    // Timeout de seguridad
    setTimeout(() => {
        clearInterval(checkPlotlyLoaded);
        if (typeof Plotly === 'undefined') {
            console.log('‚è?Timeout: Cargando Plotly manualmente...');
            cargarPlotlyManualmente();
        }
    }, 5000);
}

// Funci®Æn para ejecutar scripts de Plotly
function ejecutarScriptsPlotly() {
    const scripts = document.querySelectorAll('#plotly-container script');
    console.log(`üìú Encontrados ${scripts.length} scripts`);
    
    // Verificar si Plotly est®¢ cargado primero
    if (typeof Plotly === 'undefined') {
        console.log('‚è?Plotly no est®¢ cargado, esperando...');
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
            console.log(`‚ú?Script ${index + 1} ejecutado`);
        } catch (error) {
            console.log(`‚ù?Error en script ${index + 1}:`, error);
        }
    });
}

// Funci®Æn para cargar Plotly manualmente
function cargarPlotlyManualmente() {
    if (typeof Plotly === 'undefined') {
        console.log('üì¶ Cargando Plotly desde CDN...');
        const script = document.createElement('script');
        script.src = 'https://cdn.plot.ly/plotly-3.1.0.min.js';
        script.onload = function() {
            console.log('‚ú?Plotly cargado manualmente');
            ejecutarScriptsPlotly();
        };
        document.head.appendChild(script);
    } else {
        ejecutarScriptsPlotly();
    }
}

// Funci®Æn para recrear Plotly desde los datos
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
            
            console.log('‚ú?Gr®¢fico recreado manualmente desde datos');
        }
    } catch (error) {
        console.log('‚ù?Error recreando gr®¢fico:', error);
    }
}

// Funci®Æn para cambiar pesta√±as
async function cambiarPesta√±a(tab) {
    if (!currentSolution) return;
    
    // Si vamos a interactivo y ya tenemos el gr®¢fico, solo mostrarlo
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
                    <button class="btn-retry" onclick="cambiarPesta√±a('static')">Reintentar</button>
                </div>
            `;
            return;
        }
    }
    
    mostrarResultados(currentSolution, tab);
}

// Funci®Æn para exportar PNG
function exportarPNG() {
    if (!currentSolution?.plot) {
        alert('No hay gr√°fico para exportar');
        return;
    }

    const link = document.createElement('a');
    link.href = 'data:image/png;base64,' + currentSolution.plot;
    link.download = 'solucion_metodo_grafico.png';
    link.click();
}

// Inicializaci®Æn
document.addEventListener('DOMContentLoaded', function() {
    // Botones de optimizaci®Æn
    document.querySelectorAll('.opt-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            cambiarTipoOptimizacion(this.dataset.type);
        });
    });
    
    // Cerrar men®≤
    document.getElementById('closeMenu').addEventListener('click', function() {
        document.querySelector('.sidebar').classList.remove('active');
    });
    
    // Bot®Æn resolver
    document.querySelector('.btn-resolver').addEventListener('click', resolverProblema);
    
    // A?adir restricci®Æn
    const addButton = document.getElementById('addRestriccion');
    if (addButton) {
        addButton.addEventListener('click', function(e) {
            e.preventDefault();
            a?adirRestriccion();
        });
    }
    
    console.log('‚ú?Aplicaci®Æn inicializada. API URL:', API_URL);
});

// Remover console.log en producci®Æn (solo mantener para desarrollo)
if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    console.log = function() {}; // Silenciar console.log en producci®Æn
}