document.addEventListener('DOMContentLoaded', () => {
    const buscador = document.getElementById('buscador');
    const resultados = document.getElementById('resultados');

    buscador.addEventListener('input', () => {
        const query = buscador.value.trim();
        if (query.length >= 3) {  // Solo buscar si hay al menos 3 caracteres
            fetch(`/buscar/?query=${query}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'  // Asegura que sea AJAX
                }
            })
            .then(response => response.json())
            .then(data => {
                resultados.innerHTML = '';  // Limpia resultados anteriores
                if (data.length > 0) {
                    data.forEach(item => {
                        const div = document.createElement('div');
                        div.textContent = item.nombre;
                        div.classList.add('resultado-item');
                        
                        // Agrega el evento de clic para redirigir al mueble
                        div.addEventListener('click', () => {
                            // Suponiendo que cada item tenga un campo 'id' para identificarlo
                            window.location.href = `/mueble/${item.id}`;  // Cambia esta URL según tu estructura
                        });
                        
                        resultados.appendChild(div);
                    });
                } else {
                    resultados.innerHTML = '<div class="resultado-item">No se encontraron resultados</div>';
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            resultados.innerHTML = '';  // Limpia los resultados si la búsqueda es vacía
        }
    });
});