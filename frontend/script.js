document.addEventListener("DOMContentLoaded", () => {
    const addBtn = document.getElementById("addRestriccion");
    const restriccionesDiv = document.getElementById("restricciones");
    const resolverBtn = document.querySelector(".btn-resolver");
    const solucionDiv = document.getElementById("solucion");
    const ctx = document.getElementById("grafico").getContext("2d");

    let chart = null;

    // ➤ Añadir nuevas restricciones dinámicamente
    addBtn.addEventListener("click", (e) => {
        e.preventDefault();
        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Ej: 2x + y <= 10";
        restriccionesDiv.appendChild(input);
    });

    // ➤ Resolver problema (manda datos al backend Flask)
    resolverBtn.addEventListener("click", () => {
        // Obtener función objetivo
        const funcionObj = document.querySelector(".datos input[type='text']").value;

        // Obtener restricciones
        const restricciones = Array.from(restriccionesDiv.querySelectorAll("input"))
                                   .map(r => r.value);

        if (!funcionObj || restricciones.length === 0) {
            alert("Por favor ingrese la función objetivo y al menos una restricción.");
            return;
        }

        // Enviar al backend
        fetch("http://127.0.0.1:5000/resolver", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ funcion: funcionObj, restricciones })
        })
        .then(res => res.json())
        .then(data => {
            // Mostrar solución en la sección correspondiente
            solucionDiv.innerHTML = `
                <h3>Solución Óptima</h3>
                <p><b>Función:</b> ${data.funcion}</p>
                <p><b>Restricciones:</b> ${data.restricciones.join(", ")}</p>
                <p><b>Resultado:</b> ${data.solucion}</p>
            `;

            // ➤ Graficar (ejemplo simple)
            if (chart) chart.destroy();
            chart = new Chart(ctx, {
                type: "scatter",
                data: {
                    datasets: [
                        {
                            label: "Ejemplo Restricción 1",
                            data: [{x:0,y:6}, {x:6,y:0}],
                            borderColor: "red",
                            showLine: true
                        },
                        {
                            label: "Ejemplo Restricción 2",
                            data: [{x:0,y:4}, {x:8,y:0}],
                            borderColor: "blue",
                            showLine: true
                        }
                    ]
                },
                options: {
                    scales: {
                        x: { beginAtZero:true, title:{ display:true, text:"x" }},
                        y: { beginAtZero:true, title:{ display:true, text:"y" }}
                    }
                }
            });
        })
        .catch(err => {
            console.error("Error al conectar con el backend:", err);
            solucionDiv.innerHTML = `<p style="color:red;">Error al conectar con el servidor</p>`;
        });
    });
});
