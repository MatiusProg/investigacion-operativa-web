// VERSI車N M赤NIMA PARA PRUEBAS
console.log('? script.js cargado correctamente');

// Funci車n b芍sica para probar
function eliminarRestriccion(boton) {
    console.log('? eliminarRestriccion funciona');
    const restrictionItem = boton.closest('.restriction-item');
    if (restrictionItem) {
        restrictionItem.remove();
    }
}

function a?adirRestriccion() {
    console.log('? a?adirRestriccion funciona');
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

// Bot車n resolver b芍sico
document.addEventListener('DOMContentLoaded', function() {
    console.log('? DOM cargado');
    
    // Bot車n resolver
    const resolverBtn = document.querySelector('.btn-resolver');
    if (resolverBtn) {
        resolverBtn.addEventListener('click', function() {
            console.log('? Bot車n resolver funciona');
            alert('Funcionalidad de resolver en desarrollo');
        });
    }
    
    // Bot車n a?adir restricci車n
    const addButton = document.getElementById('addRestriccion');
    if (addButton) {
        addButton.addEventListener('click', function(e) {
            e.preventDefault();
            a?adirRestriccion();
        });
    }
    
    // Botones de optimizaci車n
    document.querySelectorAll('.opt-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('Optimizaci車n:', this.dataset.type);
            document.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
});