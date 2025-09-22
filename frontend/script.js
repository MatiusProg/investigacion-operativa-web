// VERSI��N M��NIMA PARA PRUEBAS
console.log('? script.js cargado correctamente');

// Funci��n b��sica para probar
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

// Bot��n resolver b��sico
document.addEventListener('DOMContentLoaded', function() {
    console.log('? DOM cargado');
    
    // Bot��n resolver
    const resolverBtn = document.querySelector('.btn-resolver');
    if (resolverBtn) {
        resolverBtn.addEventListener('click', function() {
            console.log('? Bot��n resolver funciona');
            alert('Funcionalidad de resolver en desarrollo');
        });
    }
    
    // Bot��n a?adir restricci��n
    const addButton = document.getElementById('addRestriccion');
    if (addButton) {
        addButton.addEventListener('click', function(e) {
            e.preventDefault();
            a?adirRestriccion();
        });
    }
    
    // Botones de optimizaci��n
    document.querySelectorAll('.opt-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('Optimizaci��n:', this.dataset.type);
            document.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
});